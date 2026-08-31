"""Task DAG loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_backlog(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        rows.append(json.loads(line))
    return rows


def next_ready(rows: list[dict[str, Any]], done: set[str]) -> dict[str, Any] | None:
    for row in rows:
        if row["id"] in done:
            continue
        deps = set(row.get("depends_on") or [])
        if deps <= done:
            return row
    return None
