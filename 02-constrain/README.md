# 02 — Constrain

**Concept:** Constrain means deciding, before the agent ever runs, exactly what it is allowed to touch — so a mistake in *reasoning* can't become a mistake in the *real world*.

## The problem it solves

An agent with tool access can do real damage from a single bad inference: a misread instruction, a prompt injection buried in a file it read, or just a model having an off moment. You cannot fix this by making the model smarter — smarter models still make mistakes. You fix it by shrinking the blast radius of any single mistake, using rules that don't depend on the model getting it right.

## Examples in this folder

### `permission-rules/`

- `settings_example.json` — a commented permission config showing `allow` / `ask` / `deny` buckets, with the blast-radius reasoning spelled out above each rule.
- `blast_radius_table.md` — 10 real agent actions rated low/medium/high blast radius, each mapped to a rule bucket and a one-line reason.

Read these together: the table is how you *decide* the buckets, the JSON is how you *encode* the decision.

### `sandbox-demo/`

- `run_sandboxed.sh` — runs an arbitrary command inside a Docker container with `--network=none` and only the project folder mounted, so even a fully compromised or malicious command can't reach the network or the rest of the filesystem.
- `README.md` — explains what this specific sandbox does and does not protect against.

## How to run

```bash
# read the permission examples (no execution needed - they're config)
cat 02-constrain/permission-rules/settings_example.json

# try the sandbox demo (requires Docker)
bash 02-constrain/sandbox-demo/run_sandboxed.sh "echo hello from inside the sandbox"
```
