"""End-to-end pipeline and payload shape."""

from __future__ import annotations

import json

from matrisk import pipeline


def test_pipeline_runs(tmp_path, raw_dir):
    payload = pipeline.run(
        raw_dir=raw_dir,
        processed_dir=tmp_path / "processed",
        dashboard_js=tmp_path / "data_inline.js",
    )
    assert payload["meta"]["pool_id"] == "ZAAUTO2024-1"
    for section in ("kpis", "ecl", "stress", "tranche_allocation",
                    "waterfall", "loss_timeseries", "stratification"):
        assert section in payload


def test_pipeline_writes_outputs(tmp_path, raw_dir):
    pipeline.run(raw_dir=raw_dir, processed_dir=tmp_path / "processed",
                 dashboard_js=tmp_path / "data_inline.js")
    pdir = tmp_path / "processed"
    assert (pdir / "stress_results.csv").exists()
    assert (pdir / "waterfall.csv").exists()
    assert (pdir / "dashboard_payload.json").exists()
    payload = json.loads((pdir / "dashboard_payload.json").read_text())
    assert payload["kpis"]["loan_count"] == 500


def test_dashboard_js_shim(tmp_path, raw_dir):
    pipeline.run(raw_dir=raw_dir, processed_dir=tmp_path / "processed",
                 dashboard_js=tmp_path / "data_inline.js")
    text = (tmp_path / "data_inline.js").read_text()
    assert text.startswith("window.DATA = {")
