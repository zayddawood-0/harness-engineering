"""
A reviewer that returns free-text prose, and a naive loop that tries to
interpret it.

Concept: VERIFY done badly. Free text forces the calling code to guess
at meaning via keyword matching - which breaks the moment the model
hedges, as real models often do.
"""


# Mocked LLM reviewer call - stands in for a real review completion.
def review_pull_request(diff_summary: str) -> str:
    if "no error handling" in diff_summary:
        return (
            "This mostly passes, though the error handling could be "
            "tighter around the network call - not blocking, but worth "
            "a follow-up."
        )
    return "Looks good, ship it."


def naive_loop_interpret(review_text: str) -> str:
    """A common but broken pattern: keyword-match for 'fail' to decide
    whether to block. This is exactly the failure logged in HARNESS.md."""
    if "fail" in review_text.lower():
        return "BLOCKED"
    return "MERGED"  # no "fail" keyword found -> treated as a pass


def main() -> None:
    diff_summary = "Added a network call to fetch pricing data, no error handling yet."
    review = review_pull_request(diff_summary)

    print(f"Reviewer said:\n  {review!r}\n")

    decision = naive_loop_interpret(review)
    print(f"Naive loop's decision: {decision}")
    print(
        "\nThe review clearly flagged a real gap (missing error handling), "
        "but because it never says the literal word 'fail', the keyword-"
        "matching loop merges it anyway. The hedge was legible to a human, "
        "invisible to the loop."
    )


if __name__ == "__main__":
    main()
