from pathlib import Path

from gbh.tasks import load_backlog, next_ready


def test_backlog_first_task():
    path = Path(__file__).resolve().parents[1] / "tasks" / "backlog.jsonl"
    rows = load_backlog(path)
    nxt = next_ready(rows, done=set())
    assert nxt is not None
    assert nxt["id"] == "A00_BOOTSTRAP"
