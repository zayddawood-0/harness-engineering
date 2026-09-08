# Hooks demo

**Concept:** VERIFY, automated. A hook is code that runs automatically at a fixed point in the agent loop (after a tool call, before the agent is allowed to stop) - it checks the agent's work with something objective instead of asking the agent to self-assess.

## The problem it solves

If verification depends on the agent remembering to run the linter or the test suite, it will eventually forget, especially under time pressure or a long task. A hook makes verification structural: it fires every time, whether the agent thinks to ask for it or not.

## What's in this folder

- `.claude/settings.json` - defines two hooks:
  - **`PostToolUse`** on `Edit`/`Write` - runs `eslint` on the file that was just changed. This is VERIFY firing immediately, catching problems while the agent still has full context on why it made the change.
  - **`Stop`** - runs `pytest` before the agent is allowed to consider its turn finished. If tests fail, the hook exits with code `2`, which blocks the stop and forces the agent to keep working. This is CORRECT: failure doesn't just get reported, it structurally prevents the loop from ending.
- `broken_file.py` - a file with an obvious lint error (`unused_variable` assigned but never read) to demonstrate the `PostToolUse` hook actually firing on a real problem.

## How to run

This demo's `settings.json` is scoped to this folder so it doesn't affect the rest of the repo. To try it in a real Claude Code session:

```bash
cd 04-verify-correct/hooks-demo
claude
# then ask Claude to edit broken_file.py - watch the PostToolUse hook fire
```

To see just the lint failure without a live session:

```bash
eslint broken_file.py   # or: python -m pyflakes broken_file.py
```

Expect a warning about `unused_variable` being assigned but never used - that's the exact class of problem the `PostToolUse` hook is designed to catch immediately after every edit, not just at the end of a session.
