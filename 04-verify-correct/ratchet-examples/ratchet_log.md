# Ratchet log — worked examples

Five realistic failures, each traced through the same four columns used in the repo-level [`HARNESS.md`](../../HARNESS.md). This is the pattern applied at example scale, so you can see the diagnosis step (which verb was missing) worked out in detail.

| What happened | Failure class | Fix | Surface updated |
|---|---|---|---|
| Reviewer subagent replied "This mostly passes, though the error handling could be tighter" and the orchestrator's keyword search for "fail" missed it, so a PR with a real gap got auto-merged. | Verify | Force the reviewer to return typed JSON (`verdict: PASS\|FAIL`) instead of prose, and validate the schema before trusting it. | `typed-output/json_reviewer.py`, `typed-output/validate.py` |
| Agent was asked to "clean up old test data" and ran a broad `DELETE FROM users WHERE created_at < ...` against the shared dev database instead of the intended sandbox table. | Constrain | Deny raw `DROP`/`DELETE`-without-`WHERE-on-primary-key` SQL from agent-executed commands; require migrations to go through a reviewed script instead of ad hoc queries. | `.claude/settings.json` deny list; `good_CLAUDE.md` database section |
| Agent read a tool's docstring that just said "fetches the record" and passed a slug where an integer ID was expected, silently returning an empty result it then reported as "record not found, deleting reference" - deleting a valid reference. | Inform | Rewrite the tool docstring to state the exact expected type and give an explicit `next_step` on empty results instead of guessing. | `ax-tool-design/good_tool.py` pattern |
| A four-step agent task failed on step 3 (a bad file edit); because nothing had been checkpointed, retrying step 3 also had to redo the now-corrupted state from steps 1-2, and the second attempt compounded the original bug. | Correct | Commit after each individually-verified step; on failure, `git checkout` back to the last good commit before retrying, instead of retrying on top of broken state. | `checkpoints/loop_with_checkpoints.sh` |
| An unattended overnight agent got stuck retrying the same failing test fix 40 times in a row, burning budget with no human aware until morning. | Escalate | Cap retries per step (e.g. 3) and define a stop condition that writes to a "Needs a Human" list instead of retrying indefinitely. | `05-complete-harness/morning-triage-loop/progress.md` "Needs a Human" section |

## The pattern

Every row is a diagnosis, not just a bug report. "What went wrong" alone doesn't tell you where to intervene - naming the missing verb tells you exactly which layer of the harness needs a new rule.
