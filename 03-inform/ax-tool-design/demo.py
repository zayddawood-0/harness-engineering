"""
Runs bad_tool and good_tool against the identical failing input and shows
what an agent's NEXT action would be in each case.

Concept: INFORM. The tool's code is not what changes agent behavior here -
it's the message that comes back. Same failure, wildly different ability
for the agent to recover on its own.
"""

from bad_tool import update_order_status as bad_update
from good_tool import update_order_status as good_update


def simulate_agent_next_action(tool_name: str, result: dict) -> str:
    """A tiny stand-in for 'what would the model do after seeing this
    tool result'. Real models are smarter than this simulation, but the
    simulation makes the information gap visible without an API call."""
    error = result.get("error")
    if error is None:
        return "Proceed - order updated successfully."

    next_step = result.get("next_step")
    if next_step:
        return f"Read next_step and retry: {next_step!r}"

    # No next_step field at all - this is the bad_tool case.
    return (
        f"Unclear how to proceed. Error was {error!r} with no explanation "
        "of cause or fix. Likely outcome: agent either gives up, asks a "
        "human, or guesses randomly and burns another turn."
    )


def main() -> None:
    order_id, status = "ORD-9999", "shipped"  # deliberately invalid order_id
    print(f"Calling update_order_status({order_id!r}, {status!r}) on both tools\n")

    bad_result = bad_update(order_id, status)
    print("bad_tool result:")
    print(f"  {bad_result}")
    print(f"  agent's next action -> {simulate_agent_next_action('bad_tool', bad_result)}\n")

    good_result = good_update(order_id, status)
    print("good_tool result:")
    print(f"  {good_result}")
    print(f"  agent's next action -> {simulate_agent_next_action('good_tool', good_result)}")


if __name__ == "__main__":
    main()
