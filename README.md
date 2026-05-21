# MatRisk AI · v1.0

> **M**aturity, **A**sset & **T**ranche **Risk** **A**nalytics **I**ntelligence
>
> A Python platform for analytics over Indian auto-loan asset-backed
> securitisations: IFRS 9 expected credit loss, RBI-aligned stress
> testing, sequential-pay waterfall mechanics, and an investor-grade
> dashboard.

[![tests](https://img.shields.io/badge/tests-41%20passing-brightgreen)]() [![coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)]()
 [![license](https://img.shields.io/badge/license-Proprietary-orange)]()

---

## Why this project exists

The pilot pool — `ZAAUTO2024-1`, an Indian retail auto-loan PTC issued
in Q4-2023 — is small (₹54.6 cr original, 500 borrowers) but
representative of the analytics challenges in the segment: 1) loan-level
heterogeneity that makes pool-level back-of-envelope ECL unreliable, 2)
multiple seniority tranches whose cash flows depend on a stochastic
default + prepayment process, and 3) regulatory pressure (RBI Master
Direction 2021, IFRS 9, Basel III) to demonstrate forward-looking,
scenario-dependent loss estimates.

MatRisk AI is the analytical kernel that does the heavy lifting for an
investor (or originator-treasury) view of such a pool: it reads the four
primary data feeds, computes the headline metrics that show up in any
trustee report, runs a five-scenario stress sweep, and ships a
JSON payload that powers an HTML dashboard. The same kernel feeds a
star-schema set of CSVs sized for direct Power BI import.

## Quick start

```bash
# 1. Clone
git clone https://github.com/ZethetaIntern/matrisk-ai
cd matrisk-ai

# 2. Install the package (Python 3.10+)
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,serve]"

# 3. Generate the seeded pool and run the full pipeline
matrisk generate
matrisk pipeline run --dashboard-out dashboard/data_inline.js

# 4. (Optional) Serve the analytics API
uvicorn matrisk.serve.app:app --reload   # then GET /health /kpis /ecl /stress
```

The raw CSVs are generated deterministically from `configs/default.yaml`
(`generate.seed`), so the entire pool — and every KPI downstream — is
fully reproducible. If `data/raw/` is missing, any command regenerates it
on demand.

Other useful commands:

```bash
matrisk kpis          # headline KPI bundle as JSON
matrisk crosscheck    # reconcile recomputed ECL vs stored provisions
matrisk stress        # print the 5-scenario stress sweep
```

## What you get

After one `pipeline run`:

```
data/processed/
├── dashboard_payload.json     ← full payload (KPIs, ECL, stress, waterfall, strata)
├── stress_results.csv         ← 5 stress scenarios × ECL + uplift
├── tranche_allocation.csv     ← bottom-up loss absorption by tranche
└── waterfall.csv              ← cash-flow line items across the loss history
dashboard/data_inline.js       ← `window.DATA = {...}` shim for the HTML dashboard
```

Sample KPI output for the pilot pool:

| Metric | Value |
|---|---|
| Pool factor | 0.582 |
| Current balance | ₹31.78 cr |
| WAC | 11.12% |
| WAM | 40.0 months |
| Weighted LTV | 70.0% |
| Weighted CIBIL | 746 |
| 30+ DPD | 14.3% of pool |
| NPA (90+) | 6.01% |
| IFRS 9 ECL | ₹1.41 cr (coverage 4.45%) |

Sample stress sweep (PD × LGD multipliers, ECL in cr):

| Scenario | PD mult | LGD mult | ECL | Uplift |
|---|---|---|---|---|
| BASE | 1.00 | 1.00 | 1.41 | — |
| MILD | 1.30 | 1.10 | 1.79 | +27% |
| MODERATE | 1.80 | 1.25 | 2.49 | +76% |
| SEVERE | 2.80 | 1.45 | 3.82 | +170% |
| CRISIS | 4.50 | 1.75 | 6.26 | +343% |

The pilot pool's 20% senior credit enhancement (12% mezzanine + 8% equity)
absorbs the stressed ECL across all five scenarios; the equity tranche
takes the first writedowns under CRISIS.

## Repository layout

```
matrisk-ai/
├── src/matrisk/                  ← installable Python package
│   ├── config.py                 ← typed loader for configs/default.yaml
│   ├── data/                     ← seeded generator, loaders, pydantic schemas
│   ├── analytics/                ← portfolio, credit (ECL), stress, waterfall
│   ├── reporting/                ← dashboard payload assembly
│   ├── cli/                      ← click-based CLI (entry point: `matrisk`)
│   ├── serve/                    ← FastAPI service (/health, /kpis, /ecl, /stress)
│   └── pipeline.py               ← end-to-end orchestration
├── tests/                        ← pytest suite (41 tests, 98% coverage)
├── configs/default.yaml          ← all policy thresholds, scenarios, tranches
├── data/
│   ├── raw/                      ← generated source + dimension CSVs
│   └── processed/                ← pipeline outputs (payload, stress, waterfall)
├── dashboard/                    ← data_inline.js shim for index.html
├── index.html                    ← standalone investor dashboard
├── dax_measure_library.dax.txt   ← 139 Power BI DAX measures
├── dax_measure_dictionary.xlsx   ← measure dictionary
├── ecl_crosscheck.xlsx           ← IFRS 9 ECL Excel crosscheck
├── waterfall_validation.xlsx     ← waterfall manual validation
├── star_schema.md                ← data-model documentation
├── technical_report.md / .pdf    ← main report
└── pyproject.toml
```

## Pipeline stages

`matrisk pipeline run` chains five steps:

1. **Ingest** — load the raw + dimension CSVs (generating them seeded if
   absent) and validate every loan row against the pydantic `LoanRecord`
   schema at the boundary.
2. **Portfolio** — compute weighted-average pool KPIs (pool factor,
   WAC, WAM, WALA, LTV, DTI, CIBIL, delinquency buckets, NPA, default
   rate, ECL coverage).
3. **Stress** — apply each scenario from `configs/default.yaml`,
   producing a long-form results frame with optional per-tranche loss
   allocation columns.
4. **Waterfall** — simulate the monthly nine-step sequential-pay
   waterfall across the loss history, returning one row per (period,
   step).
5. **Reporting** — assemble the dashboard payload and write it to
   `data/processed/dashboard_payload.json` (and an optional
   `data_inline.js` shim via `--dashboard-out`).

## Configuration

Every policy threshold lives in [`configs/default.yaml`](configs/default.yaml):

- IFRS 9 stage triggers (SICR DPD threshold, CIBIL drop, default DPD)
- LGD collar (floor / ceiling) and Stage-3 PD floor
- 5 stress scenarios with PD/LGD multipliers and macro shocks
- Tranche stack (notional, coupon, rating, rank)
- Waterfall mechanics (servicer fee, trustee fee, cash reserve target)

To run with custom thresholds:

```bash
cp configs/default.yaml configs/scenario_X.yaml
# edit ...
matrisk pipeline run --config configs/scenario_X.yaml
```

## Testing

```bash
pytest --cov=matrisk
```

The suite currently sits at **98%** across 41 tests:

| Module | Coverage |
|---|---|
| `matrisk.config` | 100% |
| `matrisk.data.generate` | 99% |
| `matrisk.data.schemas` | 100% |
| `matrisk.analytics.portfolio` | 100% |
| `matrisk.analytics.credit` | 100% |
| `matrisk.analytics.stress` | 100% |
| `matrisk.analytics.waterfall` | 100% |
| `matrisk.pipeline` | 100% |
| **TOTAL** | **98%** |

## Power BI handoff

The same star schema this engine computes is documented in
[`star_schema.md`](star_schema.md), and the 139 calculated measures in
[`dax_measure_library.dax.txt`](dax_measure_library.dax.txt) (e.g.
`[Pool Factor]`, `[30+ DPD %]`, `[Total ECL]`, `[Stressed ECL]`) are the
DAX equivalents of the Python analytics here — the two agree by
construction. The measure dictionary, ECL crosscheck, and waterfall
validation live in the `*.xlsx` workbooks at the repo root.

## Contributing

This is proprietary work product under the Indian Patents Act, 1970.
The commit history is itself part of the invention record. External
contributions are not currently accepted; please contact Zetheta
Algorithms Pvt. Ltd. directly.

## IP notice

© 2026 Zetheta Algorithms Pvt. Ltd. All rights reserved.

The MatRisk AI codebase, including all algorithmic novelty around the
LGD-collared lifetime ECL, the bottom-up loss allocation model, and the
parametric stress framework, is the exclusive property of Zetheta
Algorithms Pvt. Ltd. See `LICENSE` for the full proprietary terms.

## References

A full literature review with 20+ academic and regulatory references
appears in [`technical_report.md`](technical_report.md).
