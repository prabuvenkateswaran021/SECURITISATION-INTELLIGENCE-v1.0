"""FastAPI app: /health, /kpis, /ecl, /stress, /dashboard.

Data is loaded once at startup and cached. Run with::

    uvicorn matrisk.serve.app:app --reload
"""

from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI, Query

from ..analytics import credit, portfolio, stress
from ..config import Config, load_config
from ..data import loaders

app = FastAPI(title="MatRisk AI", version="1.0.0",
              description="Securitisation analytics kernel for Indian auto-loan ABS.")


@lru_cache(maxsize=1)
def _state() -> tuple[Config, dict]:
    cfg = load_config()
    tables = loaders.load_tables(cfg, "data/raw")
    return cfg, tables


@app.get("/health")
def health() -> dict:
    cfg, tables = _state()
    return {"status": "ok", "pool": cfg.pool.pool_id, "loans": int(len(tables["fact_loan"]))}


@app.get("/kpis")
def kpis() -> dict:
    _, tables = _state()
    return portfolio.compute_kpis(tables["fact_loan"])


@app.get("/ecl")
def ecl() -> dict:
    cfg, tables = _state()
    return credit.compute_ecl(tables["fact_loan"], cfg)["measures"]


@app.get("/stress")
def stress_sweep(
    pd_mult: float | None = Query(None, description="Override PD multiplier"),
    lgd_mult: float | None = Query(None, description="Override LGD multiplier"),
) -> dict:
    cfg, tables = _state()
    loans = tables["fact_loan"]
    if pd_mult is not None or lgd_mult is not None:
        ecl_val = stress.stress_ecl(loans, pd_mult or 1.0, lgd_mult or 1.0)
        base = stress.stress_ecl(loans, 1.0, 1.0)
        return {"custom": {"pd_mult": pd_mult or 1.0, "lgd_mult": lgd_mult or 1.0,
                           "ecl": ecl_val, "uplift_vs_base": (ecl_val - base) / base if base else 0.0}}
    return {"scenarios": stress.run_sweep(loans, cfg).to_dict(orient="records")}


@app.get("/dashboard")
def dashboard() -> dict:
    from ..pipeline import run
    return run()
