"""CSV loaders. If the raw feeds are absent, generate them on demand."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config import Config
from . import generate
from .schemas import LoanRecord

RAW_TABLES = ["fact_loan", "fact_dpd_snapshot", "fact_loss_monthly", "fact_vintage"]
DIM_TABLES = ["dim_pool", "dim_geography", "dim_vehicle", "dim_servicer",
              "dim_tranche", "dim_scenario"]


def ensure_data(cfg: Config, raw_dir: str | Path) -> Path:
    """Guarantee the raw CSVs exist; generate (seeded) if missing."""
    raw_dir = Path(raw_dir)
    loan_csv = raw_dir / "fact_loan.csv"
    if not loan_csv.exists():
        generate.write_all(cfg, raw_dir)
    return raw_dir


def load_tables(cfg: Config, raw_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Load (generating if needed) and lightly type-coerce all tables."""
    raw_dir = ensure_data(cfg, raw_dir)
    tables: dict[str, pd.DataFrame] = {}
    for name in RAW_TABLES + DIM_TABLES:
        p = Path(raw_dir) / f"{name}.csv"
        if p.exists():
            tables[name] = pd.read_csv(p)
    return tables


def validate_loans(loans: pd.DataFrame) -> int:
    """Validate every loan row against :class:`LoanRecord`. Returns row count.

    Raises ``pydantic.ValidationError`` on the first malformed row.
    """
    cols = set(LoanRecord.model_fields)
    records = loans[[c for c in loans.columns if c in cols]].to_dict(orient="records")
    for rec in records:
        rec = {**rec, "IsDefaulted": bool(rec["IsDefaulted"])}
        LoanRecord.model_validate(rec)
    return len(records)
