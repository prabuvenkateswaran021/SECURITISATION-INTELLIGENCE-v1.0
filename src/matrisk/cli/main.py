"""``matrisk`` CLI — generate data, run the pipeline, inspect KPIs."""

from __future__ import annotations

import json
from pathlib import Path

import click

from .. import __version__
from ..analytics import credit, stress
from ..config import load_config
from ..data import generate, loaders
from ..pipeline import run as run_pipeline


@click.group()
@click.version_option(__version__, prog_name="matrisk")
def cli() -> None:
    """MatRisk AI — securitisation analytics kernel."""


@cli.command("generate")
@click.option("--config", "config_path", default=None, help="Path to config YAML.")
@click.option("--raw-dir", default="data/raw", help="Output directory for CSVs.")
def generate_cmd(config_path: str | None, raw_dir: str) -> None:
    """Generate the seeded synthetic data feeds."""
    cfg = load_config(config_path)
    paths = generate.write_all(cfg, raw_dir)
    for name, p in paths.items():
        click.echo(f"  wrote {name:24s} -> {p}")
    click.secho(f"Generated {len(paths)} tables in {raw_dir}", fg="green")


@cli.group()
def pipeline() -> None:
    """Pipeline operations."""


@pipeline.command("run")
@click.option("--config", "config_path", default=None, help="Path to config YAML.")
@click.option("--raw-dir", default="data/raw")
@click.option("--processed-dir", default="data/processed")
@click.option("--dashboard-out", default=None, help="Write window.DATA JS shim here.")
def pipeline_run(config_path, raw_dir, processed_dir, dashboard_out) -> None:
    """Run ingest -> portfolio -> credit -> stress -> waterfall -> report."""
    payload = run_pipeline(config_path, raw_dir, processed_dir, dashboard_out)
    k = payload["kpis"]
    click.secho(f"\n  {payload['meta']['pool_name']}", fg="cyan", bold=True)
    click.echo(f"  Loans              {k['loan_count']}")
    click.echo(f"  Current balance    Rs {k['current_balance']/1e7:,.2f} cr")
    click.echo(f"  Pool factor        {k['pool_factor']:.3f}")
    click.echo(f"  WAC                {k['wac_pct']:.2f}%")
    click.echo(f"  WAM                {k['wam_months']:.1f} months")
    click.echo(f"  30+ DPD            {k['dpd_30plus_pct']*100:.1f}%")
    click.echo(f"  NPA (90+)          {k['npa_pct']*100:.2f}%")
    click.echo(f"  IFRS 9 ECL         Rs {payload['ecl']['total_ecl']/1e7:,.2f} cr "
               f"(coverage {payload['ecl']['ecl_coverage_pct']*100:.2f}%)")
    click.secho("Pipeline complete.", fg="green")


@cli.command("kpis")
@click.option("--config", "config_path", default=None)
@click.option("--raw-dir", default="data/raw")
def kpis_cmd(config_path, raw_dir) -> None:
    """Print the headline KPI bundle as JSON."""
    from ..analytics import portfolio
    cfg = load_config(config_path)
    tables = loaders.load_tables(cfg, raw_dir)
    click.echo(json.dumps(portfolio.compute_kpis(tables["fact_loan"]), indent=2, default=str))


@cli.command("crosscheck")
@click.option("--config", "config_path", default=None)
@click.option("--raw-dir", default="data/raw")
def crosscheck_cmd(config_path, raw_dir) -> None:
    """Reconcile recomputed ECL against the stored provisions."""
    cfg = load_config(config_path)
    tables = loaders.load_tables(cfg, raw_dir)
    res = credit.crosscheck(tables["fact_loan"], cfg)
    status = "PASS" if res["passes"] else "FAIL"
    click.secho(f"ECL crosscheck: {status}", fg="green" if res["passes"] else "red")
    click.echo(f"  stored      Rs {res['stored_ecl']/1e7:,.4f} cr")
    click.echo(f"  calculated  Rs {res['calculated_ecl']/1e7:,.4f} cr")
    click.echo(f"  rel diff    {res['rel_diff']*100:.4f}% (tol {res['tolerance']*100:.2f}%)")


@cli.command("stress")
@click.option("--config", "config_path", default=None)
@click.option("--raw-dir", default="data/raw")
def stress_cmd(config_path, raw_dir) -> None:
    """Print the stress scenario sweep."""
    cfg = load_config(config_path)
    tables = loaders.load_tables(cfg, raw_dir)
    sweep = stress.run_sweep(tables["fact_loan"], cfg)
    for _, r in sweep.iterrows():
        click.echo(f"  {r['scenario']:<18s} ECL Rs {r['ecl_cr']:6.2f} cr  "
                   f"uplift {r['uplift_vs_base']*100:+6.1f}%  cov {r['coverage_pct']*100:5.2f}%")


if __name__ == "__main__":
    cli()
