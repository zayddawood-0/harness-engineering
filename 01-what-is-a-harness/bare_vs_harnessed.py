"""
Bare vs. harnessed: the same mocked LLM call, executed two ways.

Concept: a model's *output* doesn't change based on whether you trust it.
What changes is whether anything stands between the model's words and the
real world. That gap is the harness.
"""

# Mocked LLM call — stands in for a real API call so this file runs with
# no dependencies and no API key. Real harnesses wrap a real model the
# same way: they never trust the raw completion.
def call_llm(prompt: str) -> str:
    if "clean up old records" in prompt:
        return "ACTION: rm -rf /var/data/production_db"
    return "ACTION: noop"


def execute_bare(action: str) -> None:
    """No harness: whatever the model says, happens. This is the baseline
    every real deployment starts from and must NOT ship as-is."""
    print(f"  [BARE] executing without any check: {action}")
    if action.startswith("ACTION: rm -rf"):
        print("  [BARE] >>> production database deleted. No one was asked.")
    else:
        print("  [BARE] >>> ran with no incident this time (got lucky).")


# CONSTRAIN: a permission check between the model's output and execution.
# This is the smallest possible harness — one gate, one rule.
DENY_PATTERNS = ["rm -rf", "DROP TABLE", "git push --force"]


def execute_harnessed(action: str) -> None:
    """Harnessed: the same action is checked against a deny list before
    it is allowed to run. This is CONSTRAIN in its simplest form."""
    print(f"  [HARNESSED] checking action before execution: {action}")
    for pattern in DENY_PATTERNS:
        if pattern in action:
            print(f"  [HARNESSED] >>> BLOCKED - matched deny rule '{pattern}'.")
            print("  [HARNESSED] >>> escalating to human instead of running it.")
            return
    print("  [HARNESSED] >>> passed checks, executing.")


def main() -> None:
    prompt = "Please clean up old records in the production database."
    action = call_llm(prompt)
    print(f"Model was asked: {prompt!r}")
    print(f"Model responded: {action!r}\n")

    print("Running with NO harness:")
    execute_bare(action)

    print("\nRunning the SAME action WITH a harness:")
    execute_harnessed(action)


if __name__ == "__main__":
    main()
