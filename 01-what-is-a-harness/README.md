# 01 — What is a harness?

**Concept:** A harness is everything you build around a model — permissions, tools, context, and controls — that turns a smart-but-reckless model into a system you'd actually trust to run without watching it.

## The problem it solves

If you call an LLM directly and just execute whatever it says, you get an agent with no memory of boundaries, no way to check its own work, and no concept of "ask first." It will confidently do the wrong thing exactly as fast as it does the right thing. The model isn't broken — it's just missing the scaffolding that makes autonomy safe.

## Examples in this folder

### `bare_vs_harnessed.py`

Calls the same mocked "LLM" twice with the same risky instruction ("delete the production database"):

- **Bare** — the response is executed with no checks. It just happens.
- **Harnessed** — the exact same response is passed through a permission check first. A destructive action is caught and blocked before execution.

Run it:

```bash
python bare_vs_harnessed.py
```

Expect to see the bare version execute the delete, and the harnessed version block it and explain why.

### `four_parts_demo.py`

Defines a minimal `AgentHarness` class with four attributes that every real harness has, whether it's explicit or accidental:

| Part | Question it answers |
|---|---|
| `loop` | How does the agent get from "here's a task" to "here's a result"? |
| `tools` | What can the agent actually *do* to the world? |
| `context_management` | What does the agent know at each step, and what gets dropped? |
| `controls` | What stops the agent from doing something it shouldn't? |

Run it:

```bash
python four_parts_demo.py
```

Expect to see each of the four parts printed with a concrete, non-abstract example value — not just a definition.
