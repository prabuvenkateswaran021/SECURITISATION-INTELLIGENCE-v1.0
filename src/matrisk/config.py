"""Typed configuration loaded from ``configs/default.yaml``."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "default.yaml"


class PoolCfg(BaseModel):
    pool_id: str
    pool_name: str
    asset_class: str
    cutoff_date: date
    reporting_currency: str = "INR"


class GenerateCfg(BaseModel):
    seed: int = 20240101
    n_loans: int = 500
    n_snapshot_months: int = 12
    original_pool_balance_cr: float = 54.6
    target_pool_factor: float = 0.582


class IFRS9Cfg(BaseModel):
    sicr_dpd_threshold: int = 30
    default_dpd_threshold: int = 90
    sicr_cibil_drop: int = 50
    lgd_floor: float = 0.10
    lgd_ceiling: float = 0.80
    stage3_pd_floor: float = 1.00
    stage1_pd_cap: float = 0.20
    base_lgd: float = 0.35


class ScenarioCfg(BaseModel):
    id: str
    name: str
    pd_multiplier: float
    lgd_multiplier: float
    gdp_shock_bps: int = 0
    repo_shock_bps: int = 0
    unemployment_shock_bps: int = 0


class TrancheCfg(BaseModel):
    id: str
    name: str
    rank: int
    share: float
    coupon_pct: float
    rating: str
    first_loss: bool = False


class WaterfallCfg(BaseModel):
    servicer_fee_pct: float = 0.50
    trustee_fee_pct: float = 0.05
    senior_coupon_pct: float = 8.25
    mezz_coupon_pct: float = 10.50
    cash_reserve_target_pct: float = 0.03


class Config(BaseModel):
    pool: PoolCfg
    generate: GenerateCfg = Field(default_factory=GenerateCfg)
    ifrs9: IFRS9Cfg = Field(default_factory=IFRS9Cfg)
    scenarios: list[ScenarioCfg]
    tranches: list[TrancheCfg]
    waterfall: WaterfallCfg = Field(default_factory=WaterfallCfg)

    @property
    def original_pool_balance(self) -> float:
        """Original pool balance in rupees."""
        return self.generate.original_pool_balance_cr * 1e7


def load_config(path: str | Path | None = None) -> Config:
    """Read and validate the YAML policy file into a :class:`Config`."""
    path = Path(path) if path else DEFAULT_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    return Config.model_validate(raw)
