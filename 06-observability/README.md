# 06 — Observability

**Concept:** Observability is what makes Escalate possible at all — you can't flag a problem for a human, or even notice one yourself, if the agent's run left no record of what it actually did.

## The problem it solves

An unattended agent that finishes and says "done" tells you nothing about *how* it got there: how many actions were blocked by a guardrail, whether one step cost ten times what the others did (often a sign of a planning failure or a retry loop), or whether a rule fired at all during the run. Without structured logs, every one of these signals is invisible until it becomes a visible failure.

## Examples in this folder

### `logging-demo/`

`loop_with_logging.py` — a small mocked agent loop that appends one JSON line per "beat" to `run-log.jsonl`: timestamp, actions taken, actions blocked, verdict, and token cost. This is the raw material every other tool in this folder reads.

### `cost-tracking/`

`flag_expensive_beats.py` — reads `run-log.jsonl`, computes the average cost per beat, and flags any beat costing 3x the average as a possible planning failure (the agent got stuck, over-explored, or retried excessively).

### `failure-detection/`

`alert_on_block.sh` — tails `run-log.jsonl` and prints a loud, impossible-to-miss warning the moment a beat shows `actions_blocked > 0` — i.e. the moment a guardrail actually fires, which is exactly the moment a human should know about it.

## How to run

```bash
# generate a run log
python 06-observability/logging-demo/loop_with_logging.py

# analyze it for cost anomalies
python 06-observability/cost-tracking/flag_expensive_beats.py

# watch it live for guardrail fires (run in a second terminal while
# loop_with_logging.py is running, or after, to replay the log)
bash 06-observability/failure-detection/alert_on_block.sh
```

All three tools operate on the same `run-log.jsonl` file, written to `06-observability/logging-demo/` by default — this mirrors how a real harness's observability tools all read one shared, structured log rather than each parsing raw agent transcript text differently.
