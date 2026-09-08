# 04 — Verify + Correct

**Concept:** Verify means checking whether the agent's output actually worked, using something other than the agent's own opinion. Correct means having an automatic response when verification fails — retry, roll back, or stop — instead of shipping the failure forward.

## The problem it solves

An agent that reviews its own work is grading its own homework. Even a well-intentioned model will hedge ("this mostly passes") in ways a naive loop reads as success. And even when you *do* catch a failure, if there's no defined recovery step, the failure just sits there — or worse, the loop barrels on with broken state. Verify and Correct are two halves of the same fix: catch the problem with something objective, then have an automatic, defined next step.

## Examples in this folder

### `hooks-demo/`

A `PostToolUse` hook that runs `eslint` after every file edit, and a `Stop` hook that runs `pytest` and blocks the agent from finishing if tests fail. `broken_file.py` is a deliberately lint-broken file to demonstrate the hook firing.

### `typed-output/`

- `free_text_reviewer.py` — a reviewer that returns prose. Shows exactly how a naive loop misreads a hedged "This mostly passes, though..." as a pass.
- `json_reviewer.py` — the same review, but returning a typed `{"verdict": "PASS"|"FAIL", "reasons": [...], "risk": "..."}` object, with a validator that rejects anything that doesn't match the schema.
- `validate.py` — the standalone validator (`validate_verdict(json_str)`), importable on its own.

### `ratchet-examples/`

`ratchet_log.md` — 5 real-style failure examples in a table: what happened, failure class, fix, surface updated. A worked example of the pattern in `HARNESS.md`.

### `checkpoints/`

`loop_with_checkpoints.sh` — runs an agent step, verifies it, commits on success, and on failure runs `git checkout` back to the last good commit instead of continuing on broken state.

## How to run

```bash
python 04-verify-correct/typed-output/free_text_reviewer.py
python 04-verify-correct/typed-output/json_reviewer.py
python 04-verify-correct/typed-output/validate.py
bash 04-verify-correct/checkpoints/loop_with_checkpoints.sh
```

See `hooks-demo/README.md` for how to wire up the hooks example inside a real Claude Code session.
