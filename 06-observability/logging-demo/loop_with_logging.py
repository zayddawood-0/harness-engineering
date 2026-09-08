"""
A mocked agent loop that writes one structured JSON line per beat to
run-log.jsonl.

Concept: OBSERVABILITY as the foundation for Escalate. A human (or another
tool) can only react to what got recorded - this is the recording step.
"""

import json
import random
import time
from pathlib import Path

LOG_PATH = Path(__file__).parent / "run-log.jsonl"


def run_beat(beat_num: int) -> dict:
    """Mocked single 'beat' of an agent loop: some actions attempted, some
    blocked by a guardrail, a verdict, and a token cost. Beat 4 is
    deliberately expensive and beat 6 deliberately triggers a block, to
    give the downstream analysis tools something real to find."""
    random.seed(beat_num)  # deterministic output for a reproducible demo

    actions_taken = random.randint(1, 3)
    actions_blocked = 1 if beat_num == 6 else 0
    cost = 4200 if beat_num == 4 else random.randint(200, 600)
    verdict = "PASS" if actions_blocked == 0 else "BLOCKED"

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "beat": beat_num,
        "actions_taken": actions_taken,
        "actions_blocked": actions_blocked,
        "verdict": verdict,
        "token_cost": cost,
    }


def main() -> None:
    print(f"Writing run log to {LOG_PATH}")
    with LOG_PATH.open("w", encoding="utf-8") as f:
        for beat_num in range(1, 9):
            entry = run_beat(beat_num)
            f.write(json.dumps(entry) + "\n")
            print(f"beat {beat_num}: {entry}")

    print(f"\nDone. {8} beats logged to {LOG_PATH.name}")


if __name__ == "__main__":
    main()
