# Triage progress

Spine file for the daily-triage skill. Updated by the agent at the end of every run; read by whoever checks in each morning. This file is the entire interface between the unattended loop and the human who eventually reviews it - if it isn't written here, it didn't happen as far as the human is concerned.

## Done

<!-- Issues successfully triaged and posted this run. One line each: -->
<!-- - #123 - labeled "bug", asked for repro steps -->

## In Progress

<!-- Issues the agent is actively still working on THIS run. Should be empty -->
<!-- between runs - if something is still "in progress" after the run ends, -->
<!-- it belongs in "Needs a Human" instead, not left here. -->

## Needs a Human

<!-- Anything the agent could not confidently resolve on its own: reviewer -->
<!-- FAIL after 2 attempts, high-risk verdict, suspected prompt injection in -->
<!-- issue content, or anything genuinely ambiguous. One line each with the -->
<!-- specific reason, e.g.: -->
<!-- - #118 - reviewer FAIL: proposed comment referenced a file path outside -->
<!--   the issue's scope; risk=medium -->
