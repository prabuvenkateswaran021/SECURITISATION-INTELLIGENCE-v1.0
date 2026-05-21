"""IFRS 9 ECL and crosscheck."""

from __future__ import annotations

from matrisk.analytics import credit


def test_ecl_formula_identity(loans, cfg):
    res = credit.compute_ecl(loans, cfg)
    df = res["loans"]
    # ECL must equal PD * LGD_collared * EAD row-wise.
    recomputed = (df["PD_Estimate"] * df["LGD_collared"] * df["EAD"]).clip(lower=0).sum()
    assert abs(recomputed - res["measures"]["total_ecl"]) < 1.0


def test_stage_buckets_partition(loans, cfg):
    res = credit.compute_ecl(loans, cfg)
    s = res["measures"]["stages"]
    assert s["stage1"]["count"] + s["stage2"]["count"] + s["stage3"]["count"] == len(loans)


def test_12m_plus_lifetime_equals_total(loans, cfg):
    m = credit.compute_ecl(loans, cfg)["measures"]
    assert abs((m["ecl_12month"] + m["ecl_lifetime"]) - m["total_ecl"]) < 1.0


def test_lgd_collared(loans, cfg):
    df = credit.compute_ecl(loans, cfg)["loans"]
    assert (df["LGD_collared"] >= cfg.ifrs9.lgd_floor - 1e-9).all()
    assert (df["LGD_collared"] <= cfg.ifrs9.lgd_ceiling + 1e-9).all()


def test_crosscheck_passes(loans, cfg):
    res = credit.crosscheck(loans, cfg)
    assert res["passes"]
    assert res["rel_diff"] <= res["tolerance"]
