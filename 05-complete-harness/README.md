# 05 — Complete harness

**Concept:** All five verbs (Constrain, Inform, Verify, Correct, Escalate) applied together to one real, unattended agent — a "morning triage" loop that runs on a schedule with no human watching it start.

## The problem it solves

Any single verb applied alone leaves gaps. Constrain without Verify means the agent can't do anything catastrophic, but can still confidently do the wrong *safe* thing all night. Verify without Escalate means failures get caught but nobody's ever told. A complete harness is the minimum combination where an agent can run unattended and you can trust what it did (or didn't do) by morning.

## The 8-box minimum safe harness

Every box below must be present for an agent to run unattended safely. Missing any one of them means a human has to babysit the loop.

| # | Box | Verb | What it prevents |
|---|---|---|---|
| 1 | Permission rules (allow/ask/deny) | Constrain | A single bad inference becoming irreversible real-world damage |
| 2 | Sandbox / scoped filesystem access | Constrain | Damage spreading beyond the intended project |
| 3 | Specific rules file (`CLAUDE.md`) | Inform | The agent guessing at project-specific conventions and getting them wrong |
| 4 | Precise tool docs + actionable errors | Inform | Wasted turns from the agent misusing tools it doesn't fully understand |
| 5 | Automated hooks (lint/test on every change) | Verify | A broken change surviving because no one asked the agent to check |
| 6 | Typed reviewer verdict | Verify | Hedged language slipping past a naive PASS/FAIL check |
| 7 | Checkpoint + rollback | Correct | One bad step corrupting all the good work that came before it |
| 8 | Defined escalation surface ("Needs a Human" list, retry caps) | Escalate | Silent failure - the agent either loops forever or gives up with no one told |

## Examples in this folder

### `morning-triage-loop/`

A working skeleton for an unattended agent that triages incoming issues every morning: full permission + hooks config, a reviewer subagent with a typed verdict and a deny-edit policy, the triage skill definition, a `progress.md` spine file, and the scheduled GitHub Actions workflow that runs it.

### `bad-night-demo/`

- `without_harness.md` - a step-by-step narrative of one bad night with no harness: a prompt injection leads to a `.env` read, a leak, a deleted test, and a false PASS reported by morning.
- `with_harness.md` - the identical attack sequence, this time with the 8-box harness in place: each step is blocked by naming the specific rule that stops it, ending with exactly one flagged item waiting in `progress.md` for a human.

## How to run

```bash
cat 05-complete-harness/morning-triage-loop/.claude/settings.json
cat 05-complete-harness/morning-triage-loop/.claude/agents/reviewer.md
cat 05-complete-harness/morning-triage-loop/skills/daily-triage.md
```

These are configuration and narrative examples meant to be read, adapted, and wired into a real Claude Code project - not standalone scripts.
