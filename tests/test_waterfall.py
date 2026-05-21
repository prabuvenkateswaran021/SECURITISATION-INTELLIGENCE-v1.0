"""Sequential-pay waterfall mechanics."""

from __future__ import annotations

from matrisk.analytics import waterfall


def test_waterfall_rows_per_month(tables, cfg):
    wf = waterfall.run_waterfall(tables["fact_loss_monthly"], cfg)
    months = tables["fact_loss_monthly"]["ReportingDate"].nunique()
    # 8 priority steps + 2 EOP balance rows per month.
    assert len(wf) == months * 10


def test_no_negative_payments(tables, cfg):
    wf = waterfall.run_waterfall(tables["fact_loss_monthly"], cfg)
    pay_steps = wf[~wf["Step"].str.startswith("EOP")]
    assert (pay_steps["Amount"] >= -1e-6).all()


def test_payments_never_exceed_collections(tables, cfg):
    wf = waterfall.run_waterfall(tables["fact_loss_monthly"], cfg)
    lm = tables["fact_loss_monthly"]
    for date, grp in wf.groupby("ReportingDate"):
        paid = grp[~grp["Step"].str.startswith("EOP")]["Amount"].sum()
        coll = float(lm.loc[lm["ReportingDate"] == date, "CollectionsTotal"].iloc[0])
        assert paid <= coll + 1.0


def test_credit_enhancement():
    # Senior 80 of 100 -> 20% subordination beneath it.
    assert abs(waterfall.credit_enhancement(None, 80.0, 100.0) - 0.20) < 1e-9
