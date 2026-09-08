"""Deliberately lint-broken file used to demonstrate the PostToolUse hook.

An agent (or a human) editing this file with the hooks-demo settings.json
active will see eslint/pyflakes-style output fire immediately after the
edit, because `unused_variable` is assigned but never used.
"""


def compute_total(prices: list[float]) -> float:
    unused_variable = "this triggers a lint warning: assigned but never used"
    total = 0.0
    for price in prices:
        total += price
    return total


if __name__ == "__main__":
    print(compute_total([1.0, 2.5, 3.25]))
