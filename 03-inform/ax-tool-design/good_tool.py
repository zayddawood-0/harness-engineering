"""
The same tool, redesigned for good "agent experience" (AX): a precise
docstring stating exact valid inputs, and errors that name the problem
and the fix.

Concept: INFORM. Specific docstrings let the agent form a correct plan
BEFORE calling the tool; specific errors let it self-correct AFTER a
failed call, without a human in the loop.
"""


def update_order_status(order_id: str, status: str) -> dict:
    """Update the status of an existing order.

    Args:
        order_id: Must be an existing order ID in the form "ORD-####"
            (e.g. "ORD-1001"). Use list_orders() first if you don't
            already know the ID.
        status: Must be exactly one of: "pending", "shipped",
            "delivered", "cancelled". Status can only move forward in
            that order - you cannot set "pending" on an order that is
            already "shipped" or later.

    Returns:
        dict with order_id, status, result="ok" on success, or
        dict with "error" (human-readable) and "next_step" (what the
        caller should do about it) on failure.
    """
    valid_statuses = {"pending", "shipped", "delivered", "cancelled"}
    existing_orders = {"ORD-1001", "ORD-1002", "ORD-1003"}

    if order_id not in existing_orders:
        return {
            "error": f"No order with ID '{order_id}' exists.",
            "next_step": (
                "Call list_orders() to see valid IDs, then retry with "
                "one of those. Do not guess a nearby ID."
            ),
        }

    if status not in valid_statuses:
        return {
            "error": (
                f"'{status}' is not a valid status. "
                f"Valid values are: {sorted(valid_statuses)}."
            ),
            "next_step": (
                "Retry with one of the valid values listed above - "
                "check for typos or wrong casing first."
            ),
        }

    return {"order_id": order_id, "status": status, "result": "ok"}


if __name__ == "__main__":
    result = update_order_status("ORD-9999", "shipped")
    print(result)
