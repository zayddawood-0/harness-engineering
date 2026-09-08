# Harness ratchet log

A harness is never "done." It ratchets forward: an agent fails in a new way, you diagnose which of the five verbs (Constrain, Inform, Verify, Correct, Escalate) was missing, you add the smallest fix that closes that specific gap, and the fix becomes a permanent surface (a rule, a hook, a schema, a check) so the same failure can't recur.

This file is the log of that process. Every entry answers four questions:

- **What happened** — the concrete failure, not a vague description.
- **Failure class** — which verb was missing (Constrain / Inform / Verify / Correct / Escalate).
- **Fix** — the smallest guardrail that closes this specific gap.
- **Surface updated** — the actual file/rule/hook that now encodes the fix, so it survives.

Add a new row every time an agent surprises you. If you can't point to a surface that changed, the fix didn't stick — it was advice, not a harness.

## Log

| Date | What happened | Failure class | Fix | Surface updated |
|---|---|---|---|---|
| 2026-08-14 | Agent read `.env` while "checking config for the API base URL" and pasted a live key into its chat output. | Constrain | Deny-list `.env` and `.env.*` reads outright — the agent never needed the actual secret value, only to confirm a variable existed. | `.claude/settings.json` — added `Read(./.env*)` to `deny` |
| 2026-08-22 | Reviewer subagent returned "This mostly passes, though the error handling could be tighter" and the orchestrating loop treated it as a PASS because it didn't see the word "fail." | Verify | Switched the reviewer to a typed JSON verdict (`{"verdict": "PASS"\|"FAIL", "reasons": [...], "risk": "..."}`) with a validator that rejects free text and unknown verdict values. | `04-verify-correct/typed-output/json_reviewer.py`, `validate.py` |

## Template for new entries

```
| YYYY-MM-DD | <exact failure, concrete not vague> | Constrain / Inform / Verify / Correct / Escalate | <smallest fix that closes this gap> | <file or rule that now encodes it> |
```
