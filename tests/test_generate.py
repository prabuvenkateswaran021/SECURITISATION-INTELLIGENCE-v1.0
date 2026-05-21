"""Generation: shape, determinism, and calibration."""

from __future__ import annotations

from matrisk.data import generate


def test_table_set(tables):
    for name in ("fact_loan", "fact_dpd_snapshot", "fact_loss_monthly",
                 "fact_vintage", "dim_tranche", "dim_scenario"):
        assert name in tables and len(tables[name]) > 0


def test_loan_count(loans, cfg):
    assert len(loans) == cfg.generate.n_loans


def test_deterministic(cfg):
    a = generate.generate_loans(cfg)
    b = generate.generate_loans(cfg)
    assert a["CurrentBalance"].sum() == b["CurrentBalance"].sum()
    assert a["LoanID"].tolist() == b["LoanID"].tolist()


def test_pool_factor_calibrated(loans, cfg):
    pf = loans["CurrentBalance"].sum() / loans["OriginalLoanAmount"].sum()
    assert abs(pf - cfg.generate.target_pool_factor) < 0.02


def test_balance_never_exceeds_original(loans):
    assert (loans["CurrentBalance"] <= loans["OriginalLoanAmount"] * 1.0001).all()


def test_dpd_snapshot_grain(tables, cfg):
    snaps = tables["fact_dpd_snapshot"]
    assert len(snaps) == cfg.generate.n_loans * cfg.generate.n_snapshot_months


def test_stage_consistency(loans, cfg):
    # Every 90+ DPD loan must be Stage 3.
    bad = loans[(loans["DelinquencyDays"] >= cfg.ifrs9.default_dpd_threshold)
                & (loans["IFRS9_Stage"] != 3)]
    assert bad.empty
