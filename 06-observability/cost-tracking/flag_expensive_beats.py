"""
Reads run-log.jsonl and flags any beat costing 3x the average as a
possible planning failure - the agent likely got stuck, over-explored,
or entered a retry loop.

Concept: OBSERVABILITY enabling ESCALATE. A cost spike is a signal a
human should see, but only if something is actually watching for it.
"""

import json
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "logging-demo" / "run-log.jsonl"
SPIKE_MULTIPLIER = 3


def load_beats(log_path: Path) -> list[dict]:
    if not log_path.exists():
        raise FileNotFoundError(
            f"No log at {log_path}. Run logging-demo/loop_with_logging.py first."
        )
    with log_path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def flag_expensive_beats(beats: list[dict]) -> list[dict]:
    if not beats:
        return []
    average_cost = sum(b["token_cost"] for b in beats) / len(beats)
    threshold = average_cost * SPIKE_MULTIPLIER
    return [b for b in beats if b["token_cost"] >= threshold], average_cost, threshold


def main() -> None:
    beats = load_beats(LOG_PATH)
    flagged, average_cost, threshold = flag_expensive_beats(beats)

    print(f"Analyzed {len(beats)} beats from {LOG_PATH.name}")
    print(f"Average cost per beat: {average_cost:.0f} tokens")
    print(f"Flagging threshold ({SPIKE_MULTIPLIER}x average): {threshold:.0f} tokens\n")

    if not flagged:
        print("No anomalies - no beat exceeded the threshold.")
        return

    print(f"FLAGGED {len(flagged)} beat(s) as possible planning failures:")
    for b in flagged:
        print(
            f"  beat {b['beat']}: {b['token_cost']} tokens "
            f"({b['token_cost'] / average_cost:.1f}x average) - "
            "investigate: likely got stuck, over-explored, or retried excessively."
        )


if __name__ == "__main__":
    main()
