"""
The same reviewer as free_text_reviewer.py, but forced to return a typed
JSON verdict instead of prose - and a loop that trusts the validator, not
keyword-matching.

Concept: VERIFY done well. The model can still hedge in the "reasons"
list, but the "verdict" field is constrained to exactly two values, so
the calling loop can never misread it.
"""

import json

from validate import validate_verdict


# Mocked LLM reviewer call, this time constrained to typed JSON output -
# stands in for a real API call with a JSON schema / response_format set.
def review_pull_request(diff_summary: str) -> str:
    if "no error handling" in diff_summary:
        verdict = {
            "verdict": "FAIL",
            "reasons": ["network call has no error handling around it"],
            "risk": "medium",
        }
    else:
        verdict = {"verdict": "PASS", "reasons": [], "risk": "low"}
    return json.dumps(verdict)


def loop_decide(review_json: str) -> str:
    """A loop that trusts the schema, not string-sniffing. This is the
    fix logged in HARNESS.md for the free-text hedging failure."""
    ok, message = validate_verdict(review_json)
    if not ok:
        return f"BLOCKED - malformed verdict, treat as FAIL by default: {message}"

    data = json.loads(review_json)
    if data["verdict"] == "FAIL":
        reasons = "; ".join(data["reasons"])
        return f"BLOCKED - verdict=FAIL (risk={data['risk']}): {reasons}"
    return "MERGED - verdict=PASS"


def main() -> None:
    diff_summary = "Added a network call to fetch pricing data, no error handling yet."
    review = review_pull_request(diff_summary)

    print(f"Reviewer returned:\n  {review}\n")

    decision = loop_decide(review)
    print(f"Loop's decision: {decision}")
    print(
        "\nSame underlying judgment as the free-text version, but because "
        "'verdict' can only ever be PASS or FAIL, the loop can't "
        "accidentally merge a flagged problem - there's no hedge for it "
        "to slip through."
    )


if __name__ == "__main__":
    main()
