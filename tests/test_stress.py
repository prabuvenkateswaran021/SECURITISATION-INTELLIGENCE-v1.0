"""Stress sweep and tranche loss allocation."""

from __future__ import annotations

from matrisk.analytics import stress


def test_base_equals_unstressed(loans, cfg):
    sweep = stress.run_sweep(loans, cfg)
    base = sweep[sweep["scenario_id"] == "BASE"].iloc[0]
    assert base["uplift_vs_base"] == 0.0


def test_monotonic_severity(loans, cfg):
    sweep = stress.run_sweep(loans, cfg).set_index("scenario_id")
    order = ["BASE", "MILD", "MODERATE", "SEVERE", "CRISIS"]
    ecls = [sweep.loc[s, "ecl"] for s in order]
    assert ecls == sorted(ecls)


def test_stress_caps_at_one(loans):
    # Extreme multipliers cannot push PD*LGD above EAD.
    extreme = stress.stress_ecl(loans, 100.0, 100.0)
    assert extreme <= loans["EAD"].sum() + 1.0


def test_allocation_waterfall_junior_first(cfg):
    orig = cfg.original_pool_balance
    # A loss equal to the equity thickness should fully wipe equity, spare mezz.
    equity_thickness = orig * 0.08
    alloc = stress.allocate_to_tranches(equity_thickness, cfg).set_index("tranche_id")
    assert alloc.loc["TR-C", "written_down"]
    assert not alloc.loc["TR-B", "written_down"]
    assert alloc.loc["TR-A", "loss_absorbed"] == 0.0


def test_allocation_conserves_loss(cfg):
    loss = cfg.original_pool_balance * 0.05
    alloc = stress.allocate_to_tranches(loss, cfg)
    assert abs(alloc["loss_absorbed"].sum() + alloc.attrs["unabsorbed_loss"] - loss) < 1.0
