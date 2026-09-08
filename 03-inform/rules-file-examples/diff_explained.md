# What changed from bad_CLAUDE.md to good_CLAUDE.md, and why

The bad version is not *wrong* — every line is technically good advice. The problem is that none of it is **actionable**: it doesn't tell the agent what to do differently in any specific situation it will actually face in this repo.

| Bad line | Good replacement | Why it matters |
|---|---|---|
| "Write good, clean code." | Specific stack versions + "see `app/routes/orders.py` for the pattern to copy" | "Good" is undefined. Pointing at a real file gives the agent a concrete pattern to match, not a vibe to match. |
| "Follow best practices." | The migration-ordering rule (don't drop a column same-PR as removing its usage) | This is a real incident this project had, twice. "Best practices" would never have told the agent about this specific footgun. |
| "Make sure everything works before committing." | The exact 3-step pre-commit checklist (`ruff check .`, `pytest tests/ -x`, `git diff` review) | "Works" is unverifiable by the agent. A checklist of exact commands is something it can actually run and check the exit code of. |
| "Use appropriate naming conventions." | `migrations/NNNN_description.sql`, zero-padded, "check the latest number in the folder" | Naming conventions are project-specific. Telling the agent to check the folder instead of guessing prevents migration filename collisions. |
| "Be careful with the database." | The `created_at` column requirement + why (the reporting pipeline depends on it) | "Careful" doesn't transfer. The specific schema requirement plus the *reason* lets the agent apply the rule correctly even to a new table it invents. |
| "Test your changes." | "Integration tests hit a real test database, not mocks - we've had mocked tests pass while the real migration broke prod." | Tells the agent *which kind* of test to write and *why*, based on a real past failure - see the ratchet-log pattern in `HARNESS.md`. |
| "Write helpful comments." | (removed - not project-specific, doesn't need to be in a rules file) | Generic craftsmanship advice belongs in code review norms, not a rules file the agent re-reads every session. Every line in the rules file should earn its context-window cost. |
| "Don't break anything." / "Keep the codebase maintainable." | (removed) | Same as above - unfalsifiable, un-actionable, costs context for zero behavior change. |
| "Ask if you're not sure." | (implicit, via specific escalation triggers elsewhere - e.g. the endpoint dispatch table warning) | A blanket "ask when unsure" doesn't tell the agent what "unsure" looks like. Pointing at a specific ambiguous spot (line ~40 of orders.py) is a concrete trigger, not a general disposition. |

## The pattern

Every good rule answers: **"What should the agent do differently, in what specific situation, and why?"** If a rule would survive being deleted with no behavior change, it shouldn't be in the file — it's just noise competing with the rules that matter for the model's attention.
