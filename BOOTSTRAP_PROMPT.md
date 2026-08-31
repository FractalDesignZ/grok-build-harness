# BOOTSTRAP_PROMPT.md

Paste this as the first user/system turn when attaching Grok (or any coding
agent) to a worktree that uses this harness.

---

You are implementing against `grok-build-harness`.

1. Read `AGENTS.md` and `SPEC.md` in this repo (or the consumer repo that
   vendors it).
2. Do not invent a Prime Crystal / Prime-Phase default path.
3. The first scientific question, if the consumer is GeoByteLab, is H-PATCH:
   at equal raw training bytes and matched BPB, can a cheap local byte model
   plus causal patches reduce global-backbone calls, KV-cache use, and
   measured wall-clock?
4. Work the task DAG from `tasks/backlog.jsonl` in order. Claim one task.
   Write the failing test first.
5. Submit metrics with `gbh gate submit`. Do not edit gate result files.
6. Stop at the first red causal test. Do not "fix" leakage by reading the
   future token.
7. Geometry, sheaf, Koopman, hyperbolic heads, prime-log RoPE, VSA: coefficient
   zero until their named gate exists and the patch baseline is green.

Start with `A00_BOOTSTRAP` if the consumer package does not yet import.
---
