"""CLI smoke tests via click's runner (isolated working dir)."""

from __future__ import annotations

import os
from pathlib import Path

from click.testing import CliRunner

from matrisk.cli.main import cli

CONFIG = str(Path(__file__).resolve().parents[1] / "configs" / "default.yaml")


def test_version():
    res = CliRunner().invoke(cli, ["--version"])
    assert res.exit_code == 0
    assert "1.0.0" in res.output


def test_generate_and_run(tmp_path):
    runner = CliRunner()
    raw = tmp_path / "raw"
    res = runner.invoke(cli, ["generate", "--config", CONFIG, "--raw-dir", str(raw)])
    assert res.exit_code == 0, res.output
    assert (raw / "fact_loan.csv").exists()

    res = runner.invoke(cli, [
        "pipeline", "run", "--config", CONFIG,
        "--raw-dir", str(raw), "--processed-dir", str(tmp_path / "proc")])
    assert res.exit_code == 0, res.output
    assert "Pool factor" in res.output


def test_crosscheck_and_stress(tmp_path):
    runner = CliRunner()
    raw = tmp_path / "raw"
    runner.invoke(cli, ["generate", "--config", CONFIG, "--raw-dir", str(raw)])

    res = runner.invoke(cli, ["crosscheck", "--config", CONFIG, "--raw-dir", str(raw)])
    assert res.exit_code == 0 and "PASS" in res.output

    res = runner.invoke(cli, ["stress", "--config", CONFIG, "--raw-dir", str(raw)])
    assert res.exit_code == 0 and "Crisis" in res.output

    res = runner.invoke(cli, ["kpis", "--config", CONFIG, "--raw-dir", str(raw)])
    assert res.exit_code == 0 and "pool_factor" in res.output
