"""Sequential-pay cash-flow waterfall.

Each month's collections cascade through the priority of payments:
servicer fee -> trustee fee -> senior interest -> mezz interest ->
senior principal -> mezz principal -> reserve top-up -> equity residual.
Losses are written down from the junior tranche up. Returns one row per
(period, step), the ``fact_waterfall_distribution`` grain.
"""

from __future__ import annotations

import pandas as pd

from ..config import Config


def run_waterfall(loss_monthly: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """Simulate the monthly waterfall over the loss-history horizon."""
    w = cfg.waterfall
    orig = cfg.original_pool_balance
    tranches = {t.id: t for t in cfg.tranches}
    senior, mezz, equity = tranches["TR-A"], tranches["TR-B"], tranches["TR-C"]

    bal = {"TR-A": orig * senior.share, "TR-B": orig * mezz.share, "TR-C": orig * equity.share}
    reserve = 0.0
    reserve_target = orig * w.cash_reserve_target_pct

    rows: list[dict] = []
    months = loss_monthly.sort_values("ReportingDate")
    for _, m in months.iterrows():
        period = m["ReportingDate"]
        pool_bop = float(m["BOP_Balance"])
        collections = float(m["CollectionsTotal"])
        net_loss = float(m["NetLoss_ThisMonth"])

        # Write losses down from equity upward.
        remaining_loss = net_loss
        for tid in ("TR-C", "TR-B", "TR-A"):
            absorb = min(remaining_loss, bal[tid])
            bal[tid] -= absorb
            remaining_loss -= absorb

        avail = collections

        def pay(step: str, amount: float):
            nonlocal avail
            paid = min(avail, max(amount, 0.0))
            avail -= paid
            rows.append({"ReportingDate": period, "Step": step, "Amount": round(paid, 2)})
            return paid

        pay("1. Servicer Fee", pool_bop * (w.servicer_fee_pct / 100 / 12))
        pay("2. Trustee Fee", pool_bop * (w.trustee_fee_pct / 100 / 12))
        pay("3. Senior Interest", bal["TR-A"] * (w.senior_coupon_pct / 100 / 12))
        pay("4. Mezz Interest", bal["TR-B"] * (w.mezz_coupon_pct / 100 / 12))

        # Sequential principal: senior fully amortises before mezz.
        sched_principal = float(m.get("ScheduledPrincipal", 0.0)) + float(m.get("Prepayment", 0.0))
        sr_prin = pay("5. Senior Principal", min(sched_principal, bal["TR-A"]))
        bal["TR-A"] -= sr_prin
        mz_prin = pay("6. Mezz Principal", min(max(sched_principal - sr_prin, 0.0), bal["TR-B"]))
        bal["TR-B"] -= mz_prin

        top_up = pay("7. Reserve Top-Up", max(reserve_target - reserve, 0.0))
        reserve += top_up

        pay("8. Equity Residual", avail)

        rows.append({"ReportingDate": period, "Step": "EOP Senior Balance", "Amount": round(bal["TR-A"], 2)})
        rows.append({"ReportingDate": period, "Step": "EOP Mezz Balance", "Amount": round(bal["TR-B"], 2)})

    return pd.DataFrame(rows)


def credit_enhancement(cfg: Config, senior_eop: float, total_eop: float) -> float:
    """Subordination remaining beneath the senior tranche."""
    return (total_eop - senior_eop) / total_eop if total_eop else 0.0
