# 03 — Inform

**Concept:** Inform means giving the agent exactly the knowledge it needs to act correctly — specific rules, precise tool docs, actionable errors — instead of assuming it will infer the right thing from vibes.

## The problem it solves

A model can only be as good as what it's told. Vague instructions ("follow best practices"), vague tool docstrings ("does the thing"), and vague errors ("Error 403") all push the model to guess. A guessing model is not a safety problem in the way an unconstrained model is — it's a *reliability* problem: wasted turns, wrong assumptions, retries that repeat the same mistake because the error never explained what to do differently.

## Examples in this folder

### `rules-file-examples/`

- `bad_CLAUDE.md` — a real-looking but useless rules file: generic advice that could apply to any project.
- `good_CLAUDE.md` — the same project's rules file rewritten to be specific and actionable.
- `diff_explained.md` — a line-by-line explanation of what changed and why each change matters.

### `ax-tool-design/`

"AX" = agent experience — designing tools the way you'd design an API for a very literal junior developer who cannot ask you clarifying questions mid-task.

- `bad_tool.py` — a tool function with a vague docstring and an error message that just says `"Error 403"`.
- `good_tool.py` — the same tool with a precise docstring and an error message that says exactly what went wrong and what to do next.
- `demo.py` — runs both tools against the same failing input and prints what the agent would do next in each case, side by side.

## How to run

```bash
python 03-inform/ax-tool-design/demo.py
```

Read the two rules files and the diff explanation directly — they're documentation-as-example, not scripts.
