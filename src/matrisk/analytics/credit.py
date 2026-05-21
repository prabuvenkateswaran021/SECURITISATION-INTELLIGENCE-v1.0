"""IFRS 9 expected credit loss.

ECL_loan = PD x LGD x EAD. Staging follows the config triggers:
Stage 1 (performing), Stage 2 (SICR: DPD>30 or CIBIL drop), Stage 3
(credit-impaired: DPD>=90). 12-month ECL is the Stage-1 bucket;
lifetime ECL is Stages 2 and 3.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import Config


def classify_stages(loans: pd.DataFrame, cfg: Config) -> pd.Series:
    """Recompute IFRS 9 stage from DPD + CIBIL deterioration."""
    dpd = loans["DelinquencyDays"]
    cibil_fall = loans["CIBIL_Score_Orig"] - loans["CIBIL_Score_Current"]
    stage = pd.Series(1, index=loans.index, dtype=int)
    sicr = (dpd > cfg.ifrs9.sicr_dpd_threshold) | (cibil_fall > cfg.ifrs9.sicr_cibil_drop)
    stage = stage.where(~sicr, 2)
    stage = stage.where(dpd < cfg.ifrs9.default_dpd_threshold, 3)
    return stage


def compute_ecl(loans: pd.DataFrame, cfg: Config) -> dict:
    """Loan-level ECL and the stage rollup. Returns measures + per-loan frame."""
    df = loans.copy()
    df["IFRS9_Stage"] = classify_stages(df, cfg)
    df["LGD_collared"] = df["LGD_Estimate"].clip(cfg.ifrs9.lgd_floor, cfg.ifrs9.lgd_ceiling)
    df["ECL_calc"] = (df["PD_Estimate"] * df["LGD_collared"] * df["EAD"]).clip(lower=0)

    total_ecl = float(df["ECL_calc"].sum())
    total_ead = float(df["EAD"].sum())

    stages = {}
    for s in (1, 2, 3):
        m = df["IFRS9_Stage"] == s
        ead_s = float(df.loc[m, "EAD"].sum())
        ecl_s = float(df.loc[m, "ECL_calc"].sum())
        stages[f"stage{s}"] = {
            "count": int(m.sum()),
            "balance": float(df.loc[m, "CurrentBalance"].sum()),
            "ead": ead_s,
            "ecl": ecl_s,
            "coverage_pct": ecl_s / ead_s if ead_s else 0.0,
        }

    measures = {
        "total_ecl": total_ecl,
        "total_ead": total_ead,
        "ecl_coverage_pct": total_ecl / total_ead if total_ead else 0.0,
        "ecl_12month": stages["stage1"]["ecl"],
        "ecl_lifetime": stages["stage2"]["ecl"] + stages["stage3"]["ecl"],
        "weighted_pd_pct": float((df["PD_Estimate"] * df["EAD"]).sum() / total_ead) if total_ead else 0.0,
        "weighted_lgd_pct": float((df["LGD_collared"] * df["EAD"]).sum() / total_ead) if total_ead else 0.0,
        "stages": stages,
    }
    return {"measures": measures, "loans": df}


def crosscheck(loans: pd.DataFrame, cfg: Config, tol: float = 0.01) -> dict:
    """Reconcile recomputed ECL against the stored ``ECL_Provision`` field."""
    res = compute_ecl(loans, cfg)
    stored = float(loans["ECL_Provision"].sum())
    calc = res["measures"]["total_ecl"]
    diff = calc - stored
    rel = abs(diff) / stored if stored else 0.0
    return {
        "stored_ecl": stored,
        "calculated_ecl": calc,
        "abs_diff": diff,
        "rel_diff": rel,
        "passes": rel <= tol,
        "tolerance": tol,
    }
