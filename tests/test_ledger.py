from pathlib import Path

import pytest

from gbh.ledger import record_gate, transition


def test_illegal_done_from_claimed(tmp_path: Path):
    with pytest.raises(ValueError):
        transition(tmp_path, "A00", "CLAIMED", "DONE", "agent")


def test_gate_cannot_be_silently_rewritten(tmp_path: Path):
    record_gate(tmp_path, "E6_TRAINER", "run-1", {"passed": False, "reason": "no"})
    with pytest.raises(ValueError):
        record_gate(tmp_path, "E6_TRAINER", "run-1", {"passed": True, "reason": "yes"})
    record_gate(
        tmp_path,
        "E6_TRAINER",
        "run-1",
        {"passed": True, "reason": "adr"},
        supersede=True,
        adr="docs/adr/0001.md",
    )
