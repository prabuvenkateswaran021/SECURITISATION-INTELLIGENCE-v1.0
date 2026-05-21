"""End-to-end pipeline: ingest -> portfolio -> credit -> stress -> waterfall -> report."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .analytics import credit, portfolio, stress, waterfall
from .config import Config, load_config
from .data import loaders
from .reporting import dashboard


def run(config_path: str | Path | None = None,
        raw_dir: str | Path = "data/raw",
        processed_dir: str | Path = "data/processed",
        dashboard_js: str | Path | None = None) -> dict:
    """Run the full pipeline and return the dashboard payload."""
    cfg: Config = load_config(config_path)
    tables = loaders.load_tables(cfg, raw_dir)
    loans = tables["fact_loan"]
    loss_monthly = tables["fact_loss_monthly"]

    loaders.validate_loans(loans)

    kpis = portfolio.compute_kpis(loans)
    ecl = credit.compute_ecl(loans, cfg)
    sweep = stress.run_sweep(loans, cfg)
    crisis_ecl = float(sweep.loc[sweep["scenario_id"] == "CRISIS", "ecl"].iloc[0])
    tranche_alloc = stress.allocate_to_tranches(crisis_ecl, cfg)
    wf = waterfall.run_waterfall(loss_monthly, cfg)

    strat = {
        "by_cibil_band": portfolio.stratify(loans, "CIBILBand_Curr"),
        "by_dpd_bucket": portfolio.stratify(loans, "DPD_Bucket"),
        "by_geography": portfolio.stratify(
            loans.merge(tables["dim_geography"], on="GeoKey", how="left"), "State"),
    }

    payload = dashboard.build_payload(
        cfg, kpis, ecl, sweep, tranche_alloc, wf, loss_monthly, strat)

    # Persist processed outputs.
    pdir = Path(processed_dir)
    pdir.mkdir(parents=True, exist_ok=True)
    sweep.to_csv(pdir / "stress_results.csv", index=False)
    wf.to_csv(pdir / "waterfall.csv", index=False)
    tranche_alloc.to_csv(pdir / "tranche_allocation.csv", index=False)
    dashboard.write_payload(
        payload,
        json_out=pdir / "dashboard_payload.json",
        js_out=dashboard_js,
    )
    return payload
