"""Entry point for the GitHub Issue Collector Agent.

The collector entry point will eventually coordinate these steps:

1. Load configured GitHub search queries.
2. Fetch matching issues from the GitHub API.
3. Normalize raw GitHub issue data.
4. Store normalized issue records in PostgreSQL.

For now, database write behavior is handled by issue_store.py and has already
been verified with a temporary hardcoded sample issue.
"""


def main() -> None:
    """Run the GitHub Issue Collector Agent."""

    print("GitHub Issue Collector Agent is ready.")
    print("Next step: add GitHub search query configuration.")


if __name__ == "__main__":
    main()