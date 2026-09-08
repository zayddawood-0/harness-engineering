# Rules for working in this repo

This file governs how an agent (or a human) should make changes to `harness-engineering` itself. It is the repo's own harness — dogfooding the concept it teaches.

## Language and dependencies

- Use Python 3.10+ syntax (match statements, `X | Y` union types are fine).
- Every Python example must run standalone with `python filename.py` using only the standard library, plus the `anthropic` SDK **only** where a file explicitly demonstrates real API usage. Default to mocking LLM calls — the goal is to teach the harness pattern, not to require API keys to try the repo.
- Do not add a `requirements.txt` unless an example genuinely needs a third-party package. If you do, scope it to that example's folder, not the repo root.

## Structure

- One concept per folder. Do not mix two ideas (e.g. sandboxing and typed output) into the same example — split them.
- Every folder under a numbered concept directory (`01-*` through `06-*`) must have its own `README.md` that: states the concept in one plain-English sentence, shows the problem it solves, and explains how to run the example.
- Keep Python files under 100 lines. If an example needs more than that, it is probably two examples.
- Shell scripts need a one-line comment at the top explaining what they do.

## Secrets

- Never commit API keys, tokens, `.env` files, or real credentials — not even as "obviously fake" examples that look real. Use placeholders like `sk-ant-xxxxxxxx` or `<YOUR_API_KEY_HERE>`.
- `.env` and `.env.*` must stay out of version control. If an example needs env vars, document them in that folder's README instead of a checked-in file.

## Style

- Prefer clarity over cleverness. This repo is read by students, not optimized for production throughput.
- Every code comment should connect back to the harness concept being demonstrated, not restate what the line does.
- JSON files use 2-space indentation and must be valid (`python -m json.tool file.json` should succeed).

## Changes

- If a change adds a new failure mode that a guardrail now catches, log it in [HARNESS.md](HARNESS.md) — that file is the running ratchet log for this repo's own development, not just an example artifact.
