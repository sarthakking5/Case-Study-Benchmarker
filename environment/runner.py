import json
from pathlib import Path
import click
import pandas as pd
from tabulate import tabulate

from loaders.csv_loader import process_csv
from loaders.json_loader import process_json
from loaders.validator import validate_case
from case_study.generator import save_case_study
from case_study.registry import list_cases
from environment.benchmark_env import BenchmarkEnv

@click.group()
def cli():
    """Benchmarking Framework CLI"""

@cli.command("standardize")
@click.argument("input_path", type=click.Path(exists=True))
@click.option("--case_id", default=None, help="Override case_id for the standardized case.")
def standardize(input_path, case_id):
    """Standardize a raw CSV/JSON into schema and save in data/standardized/."""
    p = Path(input_path)
    ext = p.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(p)
        data = process_csv(df, case_id=case_id or p.stem)
    elif ext == ".json":
        raw = json.loads(p.read_text())
        data = process_json(raw, case_id=case_id or p.stem)
    else:
        raise click.ClickException("Unsupported file type. Use CSV or JSON.")

    # Validate + save
    case = validate_case(data)
    out_path = save_case_study(case.model_dump(), name=case.case_id)
    click.echo(f"✅ Saved standardized case: {out_path}")

@cli.command("list")
@click.option("--dir", "dir_path", default="data/standardized/", help="Directory with standardized cases.")
def list_cmd(dir_path):
    """List available standardized case studies."""
    items = list_cases(dir_path)
    if not items:
        click.echo("No cases found.")
        return
    rows = [{"case_path": x} for x in items]
    click.echo(tabulate(rows, headers="keys"))

@cli.command("run")
@click.argument("case_path", type=click.Path(exists=True))
def run(case_path):
    """Run baseline solvers on a standardized case and print results."""
    env = BenchmarkEnv(case_path)
    res = env.run_baselines()
    click.echo(tabulate(res, headers="keys", floatfmt=".2f"))

if __name__ == "__main__":
    cli()
