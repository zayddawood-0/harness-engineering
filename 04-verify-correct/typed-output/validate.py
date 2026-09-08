"""
Standalone validator for reviewer verdicts.

Concept: VERIFY needs its own verification. A typed schema is only a real
guardrail if something actually checks the model honored the schema -
this is that check, importable on its own.
"""

import json

ALLOWED_VERDICTS = {"PASS", "FAIL"}
ALLOWED_RISKS = {"low", "medium", "high"}
REQUIRED_FIELDS = {"verdict", "reasons", "risk"}


def validate_verdict(json_str: str) -> tuple[bool, str]:
    """Validate a reviewer's JSON verdict string.

    Returns (True, "ok") if valid, or (False, <clear error message>)
    describing exactly what's wrong, so a calling loop can decide to
    retry with the specific problem named.
    """
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, f"Not valid JSON: {e}"

    if not isinstance(data, dict):
        return False, f"Expected a JSON object, got {type(data).__name__}"

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return False, f"Missing required field(s): {sorted(missing)}"

    if data["verdict"] not in ALLOWED_VERDICTS:
        return False, (
            f"'verdict' must be one of {sorted(ALLOWED_VERDICTS)}, "
            f"got {data['verdict']!r}"
        )

    if not isinstance(data["reasons"], list):
        return False, f"'reasons' must be a list, got {type(data['reasons']).__name__}"

    if data["risk"] not in ALLOWED_RISKS:
        return False, f"'risk' must be one of {sorted(ALLOWED_RISKS)}, got {data['risk']!r}"

    if data["verdict"] == "FAIL" and not data["reasons"]:
        return False, "verdict is 'FAIL' but 'reasons' is empty - a FAIL must explain why"

    return True, "ok"


if __name__ == "__main__":
    examples = [
        '{"verdict": "PASS", "reasons": [], "risk": "low"}',
        '{"verdict": "FAIL", "reasons": ["no error handling on network call"], "risk": "medium"}',
        '{"verdict": "FAIL", "reasons": [], "risk": "low"}',
        '{"verdict": "MOSTLY_PASSES", "reasons": [], "risk": "low"}',
        "This mostly passes, though...",
    ]
    for ex in examples:
        ok, message = validate_verdict(ex)
        status = "VALID" if ok else "INVALID"
        print(f"[{status}] {ex!r}\n  -> {message}\n")
