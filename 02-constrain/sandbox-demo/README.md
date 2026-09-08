# Sandbox demo

**Concept:** Permission rules constrain what an agent's *tool calls* are allowed to say. A sandbox constrains what a command can *actually do* once it runs — a second, independent layer that doesn't trust the first one.

## The problem it solves

Permission rules only work if the agent's tool-calling layer honors them. If a command itself is compromised (a malicious dependency, a prompt-injected shell command, a bug in your own rule matching), you want a second wall behind the first one. Running the command inside a container with no network access and a scoped filesystem mount means that even if something slips past your permission rules, it still can't exfiltrate data or touch anything outside the project folder.

## What this sandbox protects against

- Network exfiltration of secrets or code (`--network=none`)
- Writes to anything outside the project folder (only `PROJECT_DIR` is mounted)
- Persistent changes to the container itself (`--read-only` root filesystem, `--rm` on exit)

## What it does NOT protect against

- A command that does damage entirely within the mounted project folder (e.g. deleting your own source files) — that's a job for git checkpoints and `.gitignore`-aware backups, not sandboxing. See `04-verify-correct/checkpoints/`.
- Resource exhaustion (CPU/memory) — add `--cpus` and `--memory` flags if that's a concern in your environment.
- A supply-chain-compromised base image — pin `alpine:3.20` (or your image of choice) to a digest in real usage.

## How to run

Requires Docker installed and running.

```bash
bash run_sandboxed.sh "echo hello from inside the sandbox"
bash run_sandboxed.sh "curl https://example.com"   # fails - no network, by design
```

The first command succeeds and prints from inside the container. The second fails immediately because `--network=none` means there is no network interface to resolve or connect through at all.
