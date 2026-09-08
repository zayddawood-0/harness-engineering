"""
A tool with poor "agent experience" (AX): a vague docstring and an error
message that tells the agent nothing about what to do next.

Concept: INFORM. A tool's docstring and error messages ARE the agent's
entire understanding of that tool - there's no human to ask for
clarification mid-task.
"""


def update_order_status(order_id: str, status: str) -> dict:
    """Updates the order."""
    # Mocked backend: only a handful of order IDs "exist" and only a
    # handful of statuses are "valid" - stands in for a real API.
    valid_statuses = {"pending", "shipped", "delivered", "cancelled"}
    existing_orders = {"ORD-1001", "ORD-1002", "ORD-1003"}

    if order_id not in existing_orders:
        # BAD: no indication of what's wrong or how to fix it.
        return {"error": "Error 403"}

    if status not in valid_statuses:
        # BAD: same problem - a code with no explanation.
        return {"error": "Error 403"}

    return {"order_id": order_id, "status": status, "result": "ok"}


if __name__ == "__main__":
    result = update_order_status("ORD-9999", "shipped")
    print(result)
