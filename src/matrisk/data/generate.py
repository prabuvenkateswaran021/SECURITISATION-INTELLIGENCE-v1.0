"""Seeded synthetic-data generator for pool ZAAUTO2024-1.

The source loan tape was not committed to the repo, so this module
reproduces a plausible Indian auto-ABS pool deterministically from
``config.generate.seed``. Every figure downstream is therefore
reproducible: same seed -> identical CSVs -> identical KPIs.

The generator emits the four "raw" feeds named in the project
methodology plus the star-schema dimension tables.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from ..config import Config
from .schemas import DPD_BUCKETS

STATES = [
    ("South", "Karnataka", "Tier-1"),
    ("South", "Tamil Nadu", "Tier-1"),
    ("South", "Telangana", "Tier-1"),
    ("South", "Kerala", "Tier-2"),
    ("West", "Maharashtra", "Tier-1"),
    ("West", "Gujarat", "Tier-1"),
    ("West", "Rajasthan", "Tier-2"),
    ("North", "Delhi", "Tier-1"),
    ("North", "Haryana", "Tier-2"),
    ("North", "Punjab", "Tier-2"),
    ("North", "Uttar Pradesh", "Tier-2"),
    ("East", "West Bengal", "Tier-2"),
    ("East", "Bihar", "Tier-3"),
    ("East", "Odisha", "Tier-3"),
    ("Central", "Madhya Pradesh", "Tier-3"),
]

VEHICLES = [
    ("Maruti Suzuki", "Swift", "Hatchback"),
    ("Maruti Suzuki", "Baleno", "Hatchback"),
    ("Hyundai", "Creta", "SUV"),
    ("Hyundai", "i20", "Hatchback"),
    ("Tata", "Nexon", "SUV"),
    ("Tata", "Punch", "SUV"),
    ("Mahindra", "XUV700", "SUV"),
    ("Kia", "Seltos", "SUV"),
    ("Toyota", "Innova", "MPV"),
    ("Honda", "City", "Sedan"),
]

SERVICERS = [
    ("SRV-HDFC", "HDFC Bank", "Bank", "AAA"),
    ("SRV-ICICI", "ICICI Bank", "Bank", "AAA"),
    ("SRV-BAJAJ", "Bajaj Finance", "NBFC", "AA+"),
]

EMPLOYMENT = ["Salaried", "Self-Employed", "Professional", "Business"]


def _cibil_band(score: int) -> str:
    if score < 600:
        return "Subprime"
    if score < 650:
        return "Near Prime"
    if score < 700:
        return "Prime"
    if score < 750:
        return "Super Prime"
    return "Excellent"


def _dpd_bucket(days: int) -> str:
    if days == 0:
        return "Current"
    if days < 30:
        return "1-29 DPD"
    if days < 60:
        return "30-59 DPD"
    if days < 90:
        return "60-89 DPD"
    return "90+ DPD"


def _sma_class(days: int) -> str:
    if days == 0:
        return "Standard"
    if days <= 30:
        return "SMA-0"
    if days <= 60:
        return "SMA-1"
    if days < 90:
        return "SMA-2"
    return "NPA"


def _amortised_balance(principal: float, annual_rate: float, term: int, paid: int) -> float:
    """Outstanding principal of a level-payment loan after ``paid`` months."""
    if paid >= term:
        return 0.0
    r = annual_rate / 100.0 / 12.0
    if r <= 0:
        return principal * (1 - paid / term)
    factor = (1 + r) ** term
    bal = principal * (factor - (1 + r) ** paid) / (factor - 1)
    return max(bal, 0.0)


def generate_loans(cfg: Config) -> pd.DataFrame:
    """Generate the loan-level tape (``fact_loan`` grain)."""
    g = cfg.generate
    rng = np.random.default_rng(g.seed)
    n = g.n_loans
    cutoff = cfg.pool.cutoff_date

    # Origination dates spread over the 6-42 months before cutoff (seasoned pool).
    months_on_book = rng.integers(6, 42, n)
    orig_dates = [cutoff - relativedelta(months=int(m)) for m in months_on_book]

    original_amt = rng.lognormal(mean=np.log(1_000_000), sigma=0.45, size=n)
    original_amt = np.clip(original_amt, 250_000, 4_000_000)

    interest_rate = np.round(rng.normal(11.0, 1.6, n).clip(8.0, 16.0), 2)
    original_term = rng.choice([36, 48, 60, 72, 84], n, p=[0.12, 0.30, 0.34, 0.18, 0.06])
    remaining_term = np.maximum(original_term - months_on_book, 0)

    cibil_orig = rng.normal(745, 55, n).clip(560, 900).astype(int)
    # Current CIBIL drifts; delinquent borrowers tend to drop.
    cibil_drift = rng.normal(-3, 25, n).astype(int)
    cibil_curr = (cibil_orig + cibil_drift).clip(300, 900).astype(int)

    ltv = np.round(rng.normal(0.70, 0.10, n).clip(0.30, 0.95), 4)
    dti = np.round(rng.normal(0.34, 0.09, n).clip(0.10, 0.65), 4)

    # Delinquency: most loans current, a thin past-due tail. Worse credit -> higher DPD.
    pd_latent = (1 / (1 + np.exp((cibil_curr - 690) / 28.0)))  # 0..1, higher = riskier
    draw = rng.random(n)
    delinquency = np.zeros(n, dtype=int)
    for i in range(n):
        # ~84% current; delinquency probability rises with latent risk.
        if draw[i] < 0.86 - 0.18 * pd_latent[i]:
            delinquency[i] = 0
        else:
            delinquency[i] = int(rng.gamma(1.8, 22.0 + 55.0 * pd_latent[i]))
    delinquency = np.clip(delinquency, 0, 240)

    # Amortised current balance, then knock down a slice for prepayers.
    cur_bal = np.array(
        [_amortised_balance(original_amt[i], interest_rate[i], int(original_term[i]), int(months_on_book[i]))
         for i in range(n)]
    )
    prepay_flag = rng.random(n) < 0.10
    prepay_amt = np.where(prepay_flag, cur_bal * rng.uniform(0.2, 0.6, n), 0.0)
    cur_bal = np.maximum(cur_bal - prepay_amt, 0.0)

    # Calibrate the original pool to the configured target balance.
    scale = cfg.original_pool_balance / original_amt.sum()
    original_amt *= scale
    cur_bal *= scale
    prepay_amt *= scale

    # Nudge the aggregate pool factor toward the configured target without
    # letting any loan's balance exceed its original (capped per loan).
    natural_pf = cur_bal.sum() / original_amt.sum()
    if natural_pf > 0:
        pf_adjust = g.target_pool_factor / natural_pf
        cur_bal = np.minimum(cur_bal * pf_adjust, original_amt)

    # IFRS 9 staging.
    cibil_fall = cibil_orig - cibil_curr
    stage = np.ones(n, dtype=int)
    sicr = (delinquency > cfg.ifrs9.sicr_dpd_threshold) | (cibil_fall > cfg.ifrs9.sicr_cibil_drop)
    stage = np.where(sicr, 2, stage)
    stage = np.where(delinquency >= cfg.ifrs9.default_dpd_threshold, 3, stage)
    is_default = delinquency >= cfg.ifrs9.default_dpd_threshold

    # PD by stage.
    pd_est = np.where(
        stage == 1,
        (0.004 + 0.18 * pd_latent).clip(0.004, cfg.ifrs9.stage1_pd_cap),
        np.where(stage == 2, (0.10 + 0.45 * pd_latent).clip(0.08, 0.85), cfg.ifrs9.stage3_pd_floor),
    )
    # LGD around the base, collared.
    lgd_est = (cfg.ifrs9.base_lgd + 0.20 * (ltv - 0.70) + rng.normal(0, 0.05, n)).clip(
        cfg.ifrs9.lgd_floor, cfg.ifrs9.lgd_ceiling
    )
    ead = cur_bal.copy()
    ecl = pd_est * lgd_est * ead

    # Realised loss / recovery only on defaulted loans.
    loss_amt = np.where(is_default, ead * lgd_est, 0.0)
    recovery_amt = np.where(is_default, ead * (1 - lgd_est) * rng.uniform(0.4, 0.9, n), 0.0)
    net_loss = np.maximum(loss_amt - 0, 0.0)

    df = pd.DataFrame({
        "LoanID": [f"L{2400000 + i:07d}" for i in range(n)],
        "PoolID": cfg.pool.pool_id,
        "BorrowerID": [f"B{2400000 + i:07d}" for i in range(n)],
        "VehicleKey": rng.integers(0, len(VEHICLES), n),
        "GeoKey": rng.integers(0, len(STATES), n),
        "ServicerID": [SERVICERS[i][0] for i in rng.integers(0, len(SERVICERS), n)],
        "OriginationDateKey": [int(d.strftime("%Y%m%d")) for d in orig_dates],
        "OriginationDate": [d.isoformat() for d in orig_dates],
        "OriginalLoanAmount": np.round(original_amt, 2),
        "CurrentBalance": np.round(cur_bal, 2),
        "InterestRate": interest_rate,
        "OriginalTerm": original_term.astype(int),
        "RemainingTerm": remaining_term.astype(int),
        "MonthsOnBook": months_on_book.astype(int),
        "LTV_Current": np.round(ltv * 100, 2),
        "DTI_Ratio": np.round(dti * 100, 2),
        "CIBIL_Score_Orig": cibil_orig,
        "CIBIL_Score_Current": cibil_curr,
        "CIBILBand_Curr": [_cibil_band(int(s)) for s in cibil_curr],
        "DelinquencyDays": delinquency,
        "DPD_Bucket": [_dpd_bucket(int(d)) for d in delinquency],
        "IFRS9_Stage": stage,
        "PD_Estimate": np.round(pd_est, 6),
        "LGD_Estimate": np.round(lgd_est, 6),
        "EAD": np.round(ead, 2),
        "ECL_Provision": np.round(ecl, 2),
        "IsDefaulted": is_default,
        "LossAmount": np.round(loss_amt, 2),
        "RecoveryAmount": np.round(recovery_amt, 2),
        "NetLoss": np.round(net_loss, 2),
        "PrepaymentAmount": np.round(prepay_amt, 2),
    })
    return df


def generate_dpd_snapshots(cfg: Config, loans: pd.DataFrame) -> pd.DataFrame:
    """Monthly DPD snapshot history with roll flags (``fact_dpd_snapshot``)."""
    g = cfg.generate
    rng = np.random.default_rng(g.seed + 1)
    cutoff = cfg.pool.cutoff_date
    months = [cutoff - relativedelta(months=m) for m in range(g.n_snapshot_months - 1, -1, -1)]

    rows = []
    for _, ln in loans.iterrows():
        # Walk DPD backwards from the current value with mean-reverting noise.
        cur = int(ln.DelinquencyDays)
        path = [cur]
        for _ in range(g.n_snapshot_months - 1):
            prev = max(0, int(path[-1] - rng.choice([-30, 0, 30], p=[0.18, 0.62, 0.20])))
            path.append(prev)
        path = list(reversed(path))  # oldest -> newest
        prior_bucket = "Current"
        for mi, snap_date in enumerate(months):
            days = path[mi]
            bucket = _dpd_bucket(days)
            if mi == 0:
                roll = "Same"
            else:
                order = {b: i for i, b in enumerate(DPD_BUCKETS)}
                if order[bucket] > order[prior_bucket]:
                    roll = "Forward Roll"
                elif order[bucket] < order[prior_bucket]:
                    roll = "Backward Roll"
                else:
                    roll = "Same"
            rows.append({
                "SnapshotDate": snap_date.isoformat(),
                "SnapshotDateKey": int(snap_date.strftime("%Y%m%d")),
                "LoanID": ln.LoanID,
                "PoolID": ln.PoolID,
                "DPD_Days": days,
                "DPD_Bucket": bucket,
                "DPD_Bucket_Prior": prior_bucket,
                "RollFlag": roll,
                "CurrentBalance": round(float(ln.CurrentBalance), 2),
                "RBI_SMA_Class": _sma_class(days),
                "CureFlag": roll == "Backward Roll" and bucket == "Current",
                "RepossessionFlag": days >= 120 and rng.random() < 0.15,
                "WriteOffFlag": days >= 180 and rng.random() < 0.10,
            })
            prior_bucket = bucket
    return pd.DataFrame(rows)


def generate_loss_monthly(cfg: Config, loans: pd.DataFrame) -> pd.DataFrame:
    """Trustee monthly loss / collection series (``fact_loss_monthly``)."""
    g = cfg.generate
    rng = np.random.default_rng(g.seed + 2)
    cutoff = cfg.pool.cutoff_date
    months = [cutoff - relativedelta(months=m) for m in range(g.n_snapshot_months - 1, -1, -1)]

    bop = cfg.original_pool_balance
    rows = []
    for snap_date in months:
        mdr = float(rng.uniform(0.0008, 0.0025))
        smm = float(rng.uniform(0.008, 0.018))
        new_defaults = int(rng.integers(1, 6))
        net_loss = bop * mdr * cfg.ifrs9.base_lgd
        recoveries = net_loss * float(rng.uniform(0.3, 0.7))
        scheduled_principal = bop / 50.0
        prepay = bop * smm
        billing = bop * (cfg.pool.cutoff_date and 1) * 0.022
        coll_eff = float(rng.uniform(0.95, 0.995))
        collections = billing * coll_eff + prepay
        excess_spread = collections - net_loss - bop * (cfg.waterfall.servicer_fee_pct / 100 / 12)
        eop = max(bop - scheduled_principal - prepay - net_loss, 0.0)
        rows.append({
            "ReportingDate": snap_date.isoformat(),
            "ReportingDateKey": int(snap_date.strftime("%Y%m%d")),
            "BOP_Balance": round(bop, 2),
            "EOP_Balance": round(eop, 2),
            "NewDefaults_Count": new_defaults,
            "MonthlyDefaultRate": round(mdr, 6),
            "NetLoss_ThisMonth": round(net_loss, 2),
            "Recoveries_ThisMonth": round(recoveries, 2),
            "SMM": round(smm, 6),
            "CPR_Annualised": round(1 - (1 - smm) ** 12, 6),
            "BillingAmount": round(billing, 2),
            "CollectionsTotal": round(collections, 2),
            "CollectionEfficiency": round(coll_eff, 6),
            "ExcessSpread_Monthly": round(excess_spread, 2),
            "ScheduledPrincipal": round(scheduled_principal, 2),
            "Prepayment": round(prepay, 2),
        })
        bop = eop
    return pd.DataFrame(rows)


def generate_vintage(cfg: Config) -> pd.DataFrame:
    """Static-pool vintage curves (``fact_vintage``)."""
    rng = np.random.default_rng(cfg.generate.seed + 3)
    rows = []
    quarters = pd.date_range("2021-01-01", "2024-01-01", freq="QS")
    for q in quarters:
        vid = f"V{q.year}Q{(q.month - 1) // 3 + 1}"
        max_mob = min(48, (cfg.pool.cutoff_date.year - q.year) * 12 + (cfg.pool.cutoff_date.month - q.month))
        terminal_loss = float(rng.uniform(0.012, 0.045))
        prev_cum = 0.0
        for mob in range(0, max_mob + 1):
            # Logistic loss-timing curve approaching terminal_loss.
            cum = terminal_loss / (1 + np.exp(-(mob - 18) / 6.0))
            marginal = max(cum - prev_cum, 0.0)
            prev_cum = cum
            rows.append({
                "VintageID": vid,
                "VintageStartDateKey": int(q.strftime("%Y%m%d")),
                "MonthsOnBook": mob,
                "CumulativeNetLossRate": round(cum, 6),
                "MarginalLossRate": round(marginal, 6),
                "PoolFactor": round(max(1 - mob / 60.0, 0.0), 6),
            })
    return pd.DataFrame(rows)


def _dim_tables(cfg: Config, loans: pd.DataFrame) -> dict[str, pd.DataFrame]:
    dim_geo = pd.DataFrame(
        [{"GeoKey": i, "Region": r, "State": s, "StateTier": t} for i, (r, s, t) in enumerate(STATES)]
    )
    dim_veh = pd.DataFrame(
        [{"VehicleKey": i, "VehicleMake": mk, "VehicleModel": md, "VehicleType": vt}
         for i, (mk, md, vt) in enumerate(VEHICLES)]
    )
    dim_srv = pd.DataFrame(
        [{"ServicerID": sid, "ServicerName": nm, "ServicerType": ty, "ServicerRating": rt}
         for sid, nm, ty, rt in SERVICERS]
    )
    orig_bal = cfg.original_pool_balance
    dim_tranche = pd.DataFrame([
        {"TrancheID": t.id, "TrancheName": t.name, "TrancheRank": t.rank,
         "CreditRating": t.rating, "CouponRate_Pct": t.coupon_pct,
         "OriginalBalance_INR": round(orig_bal * t.share, 2),
         "FirstLossPosition": t.first_loss}
        for t in cfg.tranches
    ])
    dim_scenario = pd.DataFrame([
        {"ScenarioID": s.id, "ScenarioName": s.name, "PD_Multiplier": s.pd_multiplier,
         "LGD_Multiplier": s.lgd_multiplier, "Recovery_Haircut_Pct": 0.0,
         "GDP_Shock_bps": s.gdp_shock_bps, "Repo_Shock_bps": s.repo_shock_bps,
         "Unemployment_Shock_bps": s.unemployment_shock_bps}
        for s in cfg.scenarios
    ])
    dim_pool = pd.DataFrame([{
        "PoolID": cfg.pool.pool_id, "PoolName": cfg.pool.pool_name,
        "AssetClass": cfg.pool.asset_class,
        "OriginalPoolBalance_INR": round(orig_bal, 2),
        "CutoffDate": cfg.pool.cutoff_date.isoformat(),
    }])
    return {
        "dim_pool": dim_pool, "dim_geography": dim_geo, "dim_vehicle": dim_veh,
        "dim_servicer": dim_srv, "dim_tranche": dim_tranche, "dim_scenario": dim_scenario,
    }


def generate_all(cfg: Config) -> dict[str, pd.DataFrame]:
    """Produce every raw + dimension table as DataFrames."""
    loans = generate_loans(cfg)
    tables = {
        "fact_loan": loans,
        "fact_dpd_snapshot": generate_dpd_snapshots(cfg, loans),
        "fact_loss_monthly": generate_loss_monthly(cfg, loans),
        "fact_vintage": generate_vintage(cfg),
    }
    tables.update(_dim_tables(cfg, loans))
    return tables


def write_all(cfg: Config, out_dir: str | Path) -> dict[str, Path]:
    """Generate and write all tables as CSV. Returns name -> path."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for name, df in generate_all(cfg).items():
        p = out_dir / f"{name}.csv"
        df.to_csv(p, index=False)
        paths[name] = p
    return paths
