"""Parametric stress testing.

For each scenario, stressed ECL = SUMX( min(PD x pd_mult, 1) x
min(LGD x lgd_mult, 1) x EAD ). Mirrors the [Stressed ECL] DAX measure.
"""

from __future__ import annotations

import pandas as pd

from ..config import Config


def stress_ecl(loans: pd.DataFrame, pd_mult: float, lgd_mult: float,
               recovery_haircut: float = 0.0) -> float:
    """Single stressed-ECL figure under explicit multipliers."""
    pd_s = (loans["PD_Estimate"] * pd_mult).clip(upper=1.0)
    lgd_s = (loans["LGD_Estimate"] * lgd_mult * (1 + recovery_haircut)).clip(upper=1.0)
    return float((pd_s * lgd_s * loans["EAD"]).sum())


def run_sweep(loans: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """Full scenario sweep: one row per scenario with ECL, uplift, coverage."""
    base = stress_ecl(loans, 1.0, 1.0)
    total_ead = float(loans["EAD"].sum())
    rows = []
    for s in cfg.scenarios:
        ecl = stress_ecl(loans, s.pd_multiplier, s.lgd_multiplier)
        rows.append({
            "scenario_id": s.id,
            "scenario": s.name,
            "pd_multiplier": s.pd_multiplier,
            "lgd_multiplier": s.lgd_multiplier,
            "ecl": ecl,
            "ecl_cr": ecl / 1e7,
            "uplift_vs_base": (ecl - base) / base if base else 0.0,
            "coverage_pct": ecl / total_ead if total_ead else 0.0,
            "gdp_shock_bps": s.gdp_shock_bps,
            "repo_shock_bps": s.repo_shock_bps,
            "unemployment_shock_bps": s.unemployment_shock_bps,
        })
    return pd.DataFrame(rows)


def allocate_to_tranches(stressed_ecl: float, cfg: Config) -> pd.DataFrame:
    """Bottom-up loss allocation: equity absorbs first, then mezz, then senior."""
    orig = cfg.original_pool_balance
    # Tranches ranked senior->junior; absorb losses from the junior end.
    junior_first = sorted(cfg.tranches, key=lambda t: -t.rank)
    remaining = stressed_ecl
    rows = []
    for t in junior_first:
        thickness = orig * t.share
        absorbed = min(remaining, thickness)
        remaining -= absorbed
        rows.append({
            "tranche_id": t.id,
            "tranche": t.name,
            "rank": t.rank,
            "thickness": thickness,
            "loss_absorbed": absorbed,
            "loss_absorbed_pct": absorbed / thickness if thickness else 0.0,
            "written_down": absorbed >= thickness - 1.0,
        })
    df = pd.DataFrame(rows).sort_values("rank").reset_index(drop=True)
    df.attrs["unabsorbed_loss"] = remaining
    return df
