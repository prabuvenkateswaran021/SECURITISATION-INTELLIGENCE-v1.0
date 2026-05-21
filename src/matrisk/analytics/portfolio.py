"""Pool-level KPIs. Python equivalents of the foundational DAX measures.

Each function name maps to a measure family in
``dax_measure_library.dax.txt`` so the Power BI model and this engine
agree by construction.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _wavg(values: pd.Series, weights: pd.Series) -> float:
    w = weights.sum()
    return float((values * weights).sum() / w) if w else 0.0


def weighted_averages(loans: pd.DataFrame) -> dict[str, float]:
    """Balance-weighted WAC / WAM / WALA / LTV / DTI / CIBIL."""
    bal = loans["CurrentBalance"]
    return {
        "wac_pct": _wavg(loans["InterestRate"], bal),
        "wam_months": _wavg(loans["RemainingTerm"], bal),
        "wala_months": _wavg(loans["MonthsOnBook"], bal),
        "weighted_ltv_pct": _wavg(loans["LTV_Current"], bal),
        "weighted_dti_pct": _wavg(loans["DTI_Ratio"], bal),
        "weighted_cibil": _wavg(loans["CIBIL_Score_Current"], bal),
    }


def delinquency_buckets(loans: pd.DataFrame) -> dict[str, float]:
    """30+/60+/90+ DPD balance shares plus loan-count delinquency rate."""
    bal = loans["CurrentBalance"]
    total = bal.sum()
    dpd = loans["DelinquencyDays"]
    out: dict[str, float] = {}
    for thr in (30, 60, 90):
        mask = dpd >= thr
        out[f"dpd_{thr}plus_balance"] = float(bal[mask].sum())
        out[f"dpd_{thr}plus_pct"] = float(bal[mask].sum() / total) if total else 0.0
        out[f"dpd_{thr}plus_count"] = int(mask.sum())
    out["delinquency_rate_pct"] = float((dpd >= 30).sum() / len(loans)) if len(loans) else 0.0
    out["npa_balance"] = out["dpd_90plus_balance"]
    out["npa_pct"] = out["dpd_90plus_pct"]
    return out


def compute_kpis(loans: pd.DataFrame) -> dict[str, float]:
    """Headline portfolio KPI bundle (the dashboard summary card)."""
    bal = loans["CurrentBalance"]
    orig = loans["OriginalLoanAmount"]
    current_balance = float(bal.sum())
    original_balance = float(orig.sum())

    kpis: dict[str, float] = {
        "loan_count": int(len(loans)),
        "borrower_count": int(loans["BorrowerID"].nunique()),
        "original_balance": original_balance,
        "current_balance": current_balance,
        "pool_factor": current_balance / original_balance if original_balance else 0.0,
        "avg_loan_size": current_balance / len(loans) if len(loans) else 0.0,
        "total_ead": float(loans["EAD"].sum()),
        "defaulted_count": int(loans["IsDefaulted"].sum()),
        "default_rate_pct": float(loans["IsDefaulted"].sum() / len(loans)) if len(loans) else 0.0,
        "total_gross_loss": float(loans["LossAmount"].sum()),
        "total_net_loss": float(loans["NetLoss"].sum()),
        "total_recovery": float(loans["RecoveryAmount"].sum()),
        "total_prepayment": float(loans["PrepaymentAmount"].sum()),
    }
    kpis["gross_loss_rate_pct"] = (
        kpis["total_gross_loss"] / original_balance if original_balance else 0.0
    )
    rec_denom = kpis["total_gross_loss"]
    kpis["recovery_rate_pct"] = kpis["total_recovery"] / rec_denom if rec_denom else 0.0
    kpis.update(weighted_averages(loans))
    kpis.update(delinquency_buckets(loans))
    # Top-10 borrower concentration + HHI on current balance.
    by_borrower = loans.groupby("BorrowerID")["CurrentBalance"].sum().sort_values(ascending=False)
    kpis["top10_borrower_share_pct"] = (
        float(by_borrower.head(10).sum() / current_balance) if current_balance else 0.0
    )
    shares = (by_borrower / current_balance) if current_balance else by_borrower * 0
    kpis["hhi"] = float((shares ** 2).sum() * 10_000)  # 0..10000 index
    return kpis


def stratify(loans: pd.DataFrame, by: str) -> pd.DataFrame:
    """Pool stratification: balance + count + ECL by a banding column."""
    grp = loans.groupby(by).agg(
        balance=("CurrentBalance", "sum"),
        loans=("LoanID", "count"),
        ecl=("ECL_Provision", "sum"),
    ).reset_index()
    total = grp["balance"].sum()
    grp["balance_pct"] = grp["balance"] / total if total else 0.0
    return grp.sort_values("balance", ascending=False)
