"""Append-only task and gate ledger. Agents cannot rewrite history."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STATES = (
    "BACKLOG",
    "CLAIMED",
    "RED_TEST",
    "IMPLEMENTED",
    "SELF_REVIEWED",
    "INTEGRATION_TESTED",
    "PROFILED_IF_REQUIRED",
    "DONE",
    "BLOCKED",
    "REJECTED",
)

LEGAL = {
    "BACKLOG": {"CLAIMED", "REJECTED"},
    "CLAIMED": {"RED_TEST", "BACKLOG", "BLOCKED"},
    "RED_TEST": {"IMPLEMENTED", "BLOCKED", "CLAIMED"},
    "IMPLEMENTED": {"SELF_REVIEWED", "RED_TEST", "BLOCKED"},
    "SELF_REVIEWED": {"INTEGRATION_TESTED", "IMPLEMENTED", "BLOCKED"},
    "INTEGRATION_TESTED": {"PROFILED_IF_REQUIRED", "DONE", "BLOCKED"},
    "PROFILED_IF_REQUIRED": {"DONE", "BLOCKED"},
    "DONE": set(),
    "BLOCKED": {"CLAIMED", "REJECTED"},
    "REJECTED": set(),
}


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, separators=(",", ":")) + "\n")


def transition(
    ledger_dir: Path,
    task_id: str,
    src: str,
    dst: str,
    actor: str,
    note: str = "",
) -> dict[str, Any]:
    if src not in STATES or dst not in STATES:
        raise ValueError(f"unknown state {src}->{dst}")
    if dst not in LEGAL[src]:
        raise ValueError(f"illegal transition {src}->{dst}")
    if dst == "DONE" and os.environ.get("GBH_REQUIRE_GATE") == "1":
        raise ValueError("DONE requires gbh gate evaluate when GBH_REQUIRE_GATE=1")
    rec = {
        "ts": _now(),
        "task_id": task_id,
        "from": src,
        "to": dst,
        "actor": actor,
        "note": note,
    }
    append_jsonl(ledger_dir / "events.jsonl", rec)
    return rec


def record_gate(
    ledger_dir: Path,
    gate: str,
    run_id: str,
    result: dict[str, Any],
    *,
    supersede: bool = False,
    adr: str | None = None,
) -> dict[str, Any]:
    path = ledger_dir / "gates.jsonl"
    if path.exists() and not supersede:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            prev = json.loads(line)
            if prev.get("gate") == gate and prev.get("run_id") == run_id:
                raise ValueError(
                    f"gate {gate} already recorded for {run_id}; pass supersede+adr to replace"
                )
    if supersede and not adr:
        raise ValueError("supersede requires an ADR path")
    rec = {
        "ts": _now(),
        "gate": gate,
        "run_id": run_id,
        "passed": result.get("passed"),
        "raised": result.get("raised", False),
        "reason": result.get("reason"),
        "supersede": supersede,
        "adr": adr,
        "result": result,
    }
    append_jsonl(path, rec)
    return rec
