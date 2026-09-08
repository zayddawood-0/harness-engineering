# Blast radius table

Ten real agent actions, rated by what happens if the agent does this **at the wrong moment, for the wrong reason**. The rating drives the rule bucket — not how often the action is needed, not how much the agent "should" know better.

| # | Action | Blast radius | Rule bucket | Reason |
|---|---|---|---|---|
| 1 | Read a source file in the repo | Low | allow | Read-only, no state change, nothing to undo |
| 2 | Run the existing test suite | Low | allow | Read-only against the running system, side effects are local and expected |
| 3 | Run `git diff` / `git status` | Low | allow | Inspects state, changes nothing |
| 4 | Fetch a URL (`WebFetch`) | Medium | ask | Can leak context to an external server or pull untrusted/injected content back in |
| 5 | Install a new npm package | Medium | ask | Runs arbitrary install scripts and changes the dependency tree - reversible, but not free |
| 6 | Commit changes locally | Medium | ask | Reversible with `git reset`, but creates a record and can include unintended files |
| 7 | Push to a remote branch | Medium-High | ask | Visible to teammates and CI; reversible but embarrassing and noisy to undo |
| 8 | Read `.env` or any credentials file | High | deny | The only reason to read it is to use the secret - agent never needs the raw value |
| 9 | Force-push to any branch | High | deny | Overwrites remote history; can destroy a teammate's unpushed work irreversibly |
| 10 | `rm -rf` on any path | High | deny | Irreversible deletion with no confirmation step and no undo |

## How to read this table

The pattern: **low blast radius = allow, medium = ask, high = deny — no exceptions on high.** A rule that's sometimes right for high-blast-radius actions is a rule that's occasionally catastrophic. If an action genuinely needs to happen (e.g. a real force-push during a rebase cleanup), that's a human decision made outside the agent's own authority, not a case for loosening the deny rule.
