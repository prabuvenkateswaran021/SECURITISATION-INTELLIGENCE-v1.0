"""Portfolio KPI correctness."""

from __future__ import annotations

import pandas as pd

from matrisk.analytics import portfolio


def test_kpi_keys(loans):
    k = portfolio.compute_kpis(loans)
    for key in ("pool_factor", "wac_pct", "wam_months", "weighted_ltv_pct",
                "weighted_cibil", "dpd_30plus_pct", "npa_pct", "hhi"):
        assert key in k


def test_pool_factor_matches_definition(loans):
    k = portfolio.compute_kpis(loans)
    expected = loans["CurrentBalance"].sum() / loans["OriginalLoanAmount"].sum()
    assert abs(k["pool_factor"] - expected) < 1e-9


def test_weighted_average_handcheck():
    df = pd.DataFrame({
        "CurrentBalance": [100.0, 300.0],
        "InterestRate": [10.0, 12.0],
        "RemainingTerm": [12, 24], "MonthsOnBook": [6, 12],
        "LTV_Current": [50.0, 70.0], "DTI_Ratio": [20.0, 30.0],
        "CIBIL_Score_Current": [700, 800],
    })
    wa = portfolio.weighted_averages(df)
    # (10*100 + 12*300) / 400 = 11.5
    assert abs(wa["wac_pct"] - 11.5) < 1e-9


def test_dpd_thresholds_monotonic(loans):
    k = portfolio.compute_kpis(loans)
    assert k["dpd_30plus_pct"] >= k["dpd_60plus_pct"] >= k["dpd_90plus_pct"]


def test_hhi_bounds(loans):
    k = portfolio.compute_kpis(loans)
    assert 0 < k["hhi"] <= 10_000


def test_stratify_sums_to_balance(loans):
    strat = portfolio.stratify(loans, "CIBILBand_Curr")
    assert abs(strat["balance"].sum() - loans["CurrentBalance"].sum()) < 1.0
    assert abs(strat["balance_pct"].sum() - 1.0) < 1e-6
