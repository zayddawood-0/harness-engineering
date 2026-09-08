#!/usr/bin/env bash
# Runs a series of agent "steps", commits after each one that passes
# verification, and on any failure rolls back to the last good commit
# with `git checkout` instead of continuing on broken state.
set -uo pipefail

WORKDIR="$(mktemp -d)"
echo "Working in temporary repo: ${WORKDIR}"
cd "${WORKDIR}" || exit 1

git init -q
git config user.email "demo@example.com"
git config user.name "Checkpoint Demo"
echo "start" > state.txt
git add state.txt
git commit -qm "checkpoint: initial state"

# CORRECT: each "step" is a mocked agent edit. Step 3 is deliberately
# broken to demonstrate the rollback path.
run_step() {
  local step_num="$1"
  local content="$2"
  echo "${content}" >> state.txt
  echo "step ${step_num} wrote: ${content}"
}

# VERIFY: a trivial check standing in for "run tests" / "run linter".
# Real usage would call pytest, eslint, etc. and check the exit code.
verify_step() {
  if grep -q "BROKEN" state.txt; then
    return 1
  fi
  return 0
}

STEPS=("step-1-ok" "step-2-ok" "BROKEN-step-3" "step-4-ok")

for i in "${!STEPS[@]}"; do
  step_num=$((i + 1))
  echo "--- Step ${step_num} ---"
  run_step "${step_num}" "${STEPS[$i]}"

  if verify_step; then
    git add state.txt
    git commit -qm "checkpoint: step ${step_num} verified"
    echo "VERIFIED - committed as new checkpoint."
  else
    echo "FAILED verification - rolling back to last good checkpoint."
    git checkout -q -- state.txt
    echo "state.txt restored. Current committed state:"
    cat state.txt
    echo "Stopping loop - a human should look at step ${step_num} before retrying."
    break
  fi
done

echo ""
echo "Final committed history:"
git log --oneline

echo ""
echo "Cleaning up temporary repo at ${WORKDIR}"
cd - > /dev/null || exit 1
rm -rf "${WORKDIR}"
