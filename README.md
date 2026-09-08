# Harness Engineering — Crash Course Examples

A practical companion repo for the [Panaversity Agentic AI Harness Engineering crash course](https://agentfactory.panaversity.org/docs/harness-engineering-crash-course).

Every folder in this repo teaches one idea with runnable code. Each example follows the same pattern:

1. **Without the harness** — show the agent failing, doing something unsafe, or getting stuck.
2. **With the harness** — wrap the same agent with one specific fix.
3. **Result** — show the measurable difference.

No slides. No theory-only pages. Run the file, see the behavior change.

## The equation

```
Agent = Model + Harness
```

The model is the reasoning engine. It is smart, general, and — on its own — has no memory across sessions, no permission system, no way to check its own work, and no idea when to stop and ask for help. The **harness** is everything you build around the model to make it trustworthy enough to run unattended: the loop that drives it, the tools it can call, the context it sees, and the controls that keep it inside safe boundaries.

A brilliant model with no harness is a brilliant intern with no manager, no checklist, and admin access to production. Most agent failures are not model failures — they are harness gaps.

## The five verbs

Harness engineering is the discipline of applying five verbs to every agent loop, repeatedly, until the failure rate is acceptable:

| Verb | Question it answers | What it looks like in practice |
|---|---|---|
| **Constrain** | What is the agent *allowed* to do? | Permission rules, sandboxes, allow/ask/deny lists |
| **Inform** | Does the agent *know* enough to act correctly? | Rules files, tool docstrings, error messages |
| **Verify** | Did the agent's output actually work? | Hooks, typed output, linters, test runs |
| **Correct** | What happens when verification fails? | Retries, checkpoints, rollback, re-prompting |
| **Escalate** | When should a human take over? | Confidence thresholds, flagged items, stop conditions |

These are not a one-time setup. They are a loop: run the agent, watch it fail in a new way, add one guardrail that closes that specific gap, and move on. See [HARNESS.md](HARNESS.md) for the running log of that process.

## Folder map

| Folder | Verb / Concept | What it demonstrates |
|---|---|---|
| [`01-what-is-a-harness/`](01-what-is-a-harness/) | Foundation | Bare LLM call vs. one wrapped in basic controls; the four parts of any harness (loop, tools, context management, controls) |
| [`02-constrain/`](02-constrain/) | Constrain | Permission rules by blast radius; sandboxing with no network access |
| [`03-inform/`](03-inform/) | Inform | Vague vs. specific rules files; vague vs. specific tool docstrings and errors |
| [`04-verify-correct/`](04-verify-correct/) | Verify + Correct | Hooks that block on lint/test failure; typed JSON verdicts vs. free text; checkpoint-and-rollback loops |
| [`05-complete-harness/`](05-complete-harness/) | All five verbs | A full 8-box minimum safe harness for an unattended "morning triage" agent, plus a bad-night-vs-harnessed-night narrative |
| [`06-observability/`](06-observability/) | Escalate (via visibility) | Structured run logging, cost-anomaly flagging, and guardrail-fire alerting |

## How to run examples

Every example is self-contained and uses only the Python standard library (LLM calls are mocked — no API key required to run the demos).

```bash
# from any concept folder
python <example>.py

# shell scripts
bash <example>.sh
```

Each concept folder has its own `README.md` with the specific run instructions and expected output for that example. Start at `01-what-is-a-harness/` and work down — later folders assume you've seen the earlier concepts.

## Repo rules

See [CLAUDE.md](CLAUDE.md) for the rules this repo holds itself to (Python version, folder structure, secrets policy). See [HARNESS.md](HARNESS.md) for the ratchet log template used throughout the examples.
