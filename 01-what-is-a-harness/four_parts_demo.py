"""
The four parts of any agent harness, made concrete.

Concept: "harness" sounds abstract until you name its parts. Every agent
system — however informal — has these four pieces, even if some of them
are just "whatever the developer didn't think about."
"""

from dataclasses import dataclass


@dataclass
class AgentHarness:
    loop: str               # how the agent moves from task -> result
    tools: str               # what the agent can actually do to the world
    context_management: str  # what the agent knows at each step
    controls: str            # what stops it from doing the wrong thing

    def describe(self) -> None:
        print("loop:")
        print(f"  {self.loop}\n")
        print("tools:")
        print(f"  {self.tools}\n")
        print("context_management:")
        print(f"  {self.context_management}\n")
        print("controls:")
        print(f"  {self.controls}\n")


def main() -> None:
    # A concrete example: a harness for a daily triage agent that reads
    # GitHub issues and drafts responses. Each value below is a real
    # design decision, not a placeholder.
    triage_harness = AgentHarness(
        loop=(
            "Read next open issue -> draft a response -> run it past the "
            "reviewer subagent -> if PASS, post; if FAIL, skip and flag "
            "for a human -> repeat until issue queue is empty."
        ),
        tools=(
            "github_read_issue(id), github_post_comment(id, text), "
            "github_add_label(id, label). Notably NOT: github_close_issue "
            "or github_delete_repo - those aren't exposed as tools at all."
        ),
        context_management=(
            "Each issue is handled in its own fresh context window with "
            "only that issue's thread + the last 5 similar resolved "
            "issues, not the entire repo history - keeps the model "
            "focused and avoids stale context bleeding between issues."
        ),
        controls=(
            "Permission rule denies force-push and file deletion outright; "
            "a PostToolUse hook lints any code the agent proposes; a "
            "reviewer subagent must return a typed PASS verdict before "
            "anything gets posted publicly."
        ),
    )

    print("AgentHarness - four parts, one concrete example each:\n")
    triage_harness.describe()


if __name__ == "__main__":
    main()
