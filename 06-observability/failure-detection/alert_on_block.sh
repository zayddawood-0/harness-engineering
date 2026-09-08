#!/usr/bin/env bash
# Tails run-log.jsonl and prints a loud warning the instant a beat shows
# actions_blocked > 0 - i.e. the moment a guardrail actually fires.
set -uo pipefail

LOG_PATH="$(dirname "$0")/../logging-demo/run-log.jsonl"

if [ ! -f "${LOG_PATH}" ]; then
  echo "No log found at ${LOG_PATH}"
  echo "Run: python ../logging-demo/loop_with_logging.py first."
  exit 1
fi

echo "Watching ${LOG_PATH} for guardrail fires (actions_blocked > 0)..."
echo "---"

# ESCALATE: this is the whole point of an alert script - a guardrail
# firing is exactly the kind of event a human should be told about
# immediately, not discover by reading a log the next morning.
while IFS= read -r line; do
  blocked=$(echo "${line}" | python -c "import json,sys; print(json.load(sys.stdin).get('actions_blocked', 0))" 2>/dev/null || echo 0)
  beat=$(echo "${line}" | python -c "import json,sys; print(json.load(sys.stdin).get('beat', '?'))" 2>/dev/null || echo "?")

  if [ "${blocked}" != "0" ] && [ -n "${blocked}" ]; then
    echo ""
    echo "!!! GUARDRAIL FIRED on beat ${beat} - actions_blocked=${blocked} !!!"
    echo "!!! A human should review this run before it continues.        !!!"
    echo ""
  else
    echo "beat ${beat}: clean (actions_blocked=0)"
  fi
done < "${LOG_PATH}"

echo "---"
echo "Finished reading log. (In production, replace the while-read loop"
echo "with 'tail -f' to watch a live-growing log instead of a finished one.)"
