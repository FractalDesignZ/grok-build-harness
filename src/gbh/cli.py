"""gbh CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table

from gbh.doctor import write_report
from gbh.gates import evaluate
from gbh.ledger import record_gate, transition
from gbh.tasks import load_backlog, next_ready

app = typer.Typer(no_args_is_help=True, add_completion=False)
gate_app = typer.Typer(no_args_is_help=True)
task_app = typer.Typer(no_args_is_help=True)
sources_app = typer.Typer(no_args_is_help=True)
app.add_typer(gate_app, name="gate")
app.add_typer(task_app, name="task")
app.add_typer(sources_app, name="sources")
console = Console()


@app.command()
def doctor(out: Path = Path("reports/doctor.json")) -> None:
    report = write_report(out)
    console.print_json(data=report)
    console.print(f"[dim]wrote {out}[/dim]")


@gate_app.command("evaluate")
def gate_evaluate(
    gate: str = typer.Option(...),
    metrics: Path = typer.Option(...),
    run_id: str = typer.Option("demo"),
    ledger: Path = Path("ledger"),
    out: Optional[Path] = None,
    supersede: bool = False,
    adr: Optional[str] = None,
) -> None:
    payload = json.loads(metrics.read_text(encoding="utf-8"))
    result = evaluate(gate, payload)
    record_gate(
        ledger,
        gate,
        run_id,
        result.model_dump(),
        supersede=supersede,
        adr=adr,
    )
    text = result.model_dump_json(indent=2)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    console.print(text)
    raise typer.Exit(code=0 if result.passed and not result.raised else 2)


@task_app.command("next")
def task_next(backlog: Path = Path("tasks/backlog.jsonl")) -> None:
    rows = load_backlog(backlog)
    nxt = next_ready(rows, done=set())
    if nxt is None:
        console.print("no ready task")
        raise typer.Exit(1)
    console.print_json(data=nxt)


@task_app.command("transition")
def task_transition(
    task_id: str,
    src: str = typer.Option(..., "--from"),
    dst: str = typer.Option(..., "--to"),
    actor: str = "agent",
    note: str = "",
    ledger: Path = Path("ledger"),
) -> None:
    rec = transition(ledger, task_id, src, dst, actor, note)
    console.print_json(data=rec)


@sources_app.command("check")
def sources_check(
    lock: Path = Path("manifests/sources.lock.yaml"),
    allow_example: bool = False,
) -> None:
    if not lock.exists():
        console.print(f"missing lock: {lock}")
        raise typer.Exit(1)
    data = yaml.safe_load(lock.read_text(encoding="utf-8")) or {}
    if data.get("example") and not allow_example:
        console.print("example lock is not valid for screening/confirmation")
        raise typer.Exit(2)
    rows = data.get("sources") or []
    table = Table("id", "revision")
    bad = False
    for row in rows:
        rev = str(row.get("revision") or "")
        table.add_row(str(row.get("id")), rev)
        if not row.get("example") and (not rev or rev in {"main", "master"}):
            bad = True
    console.print(table)
    if bad:
        console.print("unlocked revision in non-example source")
        raise typer.Exit(2)


if __name__ == "__main__":
    app()
