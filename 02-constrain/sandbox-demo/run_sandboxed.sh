#!/usr/bin/env bash
# Runs a command inside a network-isolated Docker container with only the
# current project folder mounted, so a compromised or malicious agent
# command cannot reach the network or read/write anything outside the project.
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 \"<command to run inside the sandbox>\""
  exit 1
fi

COMMAND="$*"
PROJECT_DIR="$(pwd)"

echo "Sandbox: no network, only ${PROJECT_DIR} mounted (read-write) as /workspace"
echo "Command: ${COMMAND}"
echo "---"

# CONSTRAIN: --network=none removes network access entirely (no exfiltration,
# no downloading a second-stage payload); the bind mount is the ONLY path in
# or out of the container, and nothing outside PROJECT_DIR is reachable.
docker run \
  --rm \
  --network=none \
  --read-only \
  --tmpfs /tmp \
  -v "${PROJECT_DIR}:/workspace" \
  -w /workspace \
  --user "$(id -u):$(id -g)" \
  alpine:3.20 \
  sh -c "${COMMAND}"

echo "---"
echo "Sandbox exited. Nothing outside ${PROJECT_DIR} could have been touched."
