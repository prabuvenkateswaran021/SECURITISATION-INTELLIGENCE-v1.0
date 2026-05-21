"""Assemble the JSON payload that powers the HTML dashboard."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from ..config import Config


def build_payload(cfg: Config, kpis: dict, ecl: dict, stress: pd.DataFrame,
                  tranche_alloc: pd.DataFrame, waterfall: pd.DataFrame,
                  loss_monthly: pd.DataFrame, strat: dict[str, pd.DataFrame]) -> dict:
    """Combine analytics outputs into a single serialisable dashboard payload."""
    return {
        "meta": {
            "pool_id": cfg.pool.pool_id,
            "pool_name": cfg.pool.pool_name,
            "cutoff_date": cfg.pool.cutoff_date.isoformat(),
            "currency": cfg.pool.reporting_currency,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine_version": "1.0.0",
        },
        "kpis": kpis,
        "ecl": ecl["measures"],
        "stress": stress.to_dict(orient="records"),
        "tranche_allocation": tranche_alloc.to_dict(orient="records"),
        "waterfall": waterfall.to_dict(orient="records"),
        "loss_timeseries": loss_monthly[
            ["ReportingDate", "BOP_Balance", "NetLoss_ThisMonth",
             "MonthlyDefaultRate", "CPR_Annualised", "CollectionEfficiency"]
        ].to_dict(orient="records"),
        "stratification": {k: v.to_dict(orient="records") for k, v in strat.items()},
    }


def write_payload(payload: dict, json_out: str | Path | None = None,
                  js_out: str | Path | None = None) -> dict[str, Path]:
    """Write the payload as JSON and/or a ``window.DATA = {...}`` JS shim."""
    written: dict[str, Path] = {}
    blob = json.dumps(payload, indent=2, default=str)
    if json_out:
        p = Path(json_out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(blob, encoding="utf-8")
        written["json"] = p
    if js_out:
        p = Path(js_out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"window.DATA = {blob};\n", encoding="utf-8")
        written["js"] = p
    return written
