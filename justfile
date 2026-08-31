set dotenv-load := false

default:
    @just --list

setup:
    uv sync --extra dev

doctor:
    uv run gbh doctor

lint:
    uv run ruff check src tests

typecheck:
    @echo "mypy is optional; ruff is the default gate"

test:
    uv run pytest -q

test-fast:
    uv run pytest -q tests/test_gates.py tests/test_ledger.py tests/test_tasks.py

test-causal:
    uv run pytest -q tests/test_causal_stub.py

gate-demo:
    uv run gbh gate evaluate --gate E6_TRAINER --metrics fixtures/e6_trainer_fail.json
    uv run gbh gate evaluate --gate E6_TRAINER --metrics fixtures/e6_trainer_pass.json --out /tmp/gbh-demo-pass.json

lock-check:
    uv run gbh sources check --lock manifests/sources.lock.example.yaml --allow-example

smoke:
    uv run gbh doctor
    uv run pytest -q tests/test_gates.py
