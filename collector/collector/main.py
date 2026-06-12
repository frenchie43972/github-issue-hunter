"""GitHub Issue Collector Agent entry point.

This module coordinates the first working collector flow:

1. Load configured GitHub issue search queries.
2. Fetch matching issues from the GitHub REST API.
3. Normalize raw GitHub API issue objects.
4. Store normalized issue records in PostgreSQL.

The collector does not score issues yet. Its current responsibility is reliable
collection and persistence.
"""

import httpx
import time

from collector.github_client import search_issues
from collector.issue_normalizer import normalize_github_issue
from collector.issue_store import upsert_github_issue
from collector.search_queries import SEARCH_QUERIES


def main() -> None:
    """Run all configured GitHub issue searches and store valid results."""

    total_saved = 0
    total_skipped = 0
    total_failed_queries = 0

    print("GitHub Issue Collector Agent started.")

    for search_query in SEARCH_QUERIES:
        saved_for_query = 0
        skipped_for_query = 0

        print("")
        print(f"Running search: {search_query.name}")
        print(f"Query: {search_query.query}")

        try:
            raw_issues = search_issues(query=search_query.query, per_page=5)

            for raw_issue in raw_issues:
                normalized_issue = normalize_github_issue(
                    raw_issue=raw_issue,
                    source_query=search_query.query,
                )

                if normalized_issue is None:
                    skipped_for_query += 1
                    total_skipped += 1
                    continue

                upsert_github_issue(normalized_issue)
                saved_for_query += 1
                total_saved += 1

            print(
                f"Finished search: {search_query.name} "
                f"saved={saved_for_query} skipped={skipped_for_query}"
            )

        except httpx.HTTPStatusError as error:
            total_failed_queries += 1
            status_code = error.response.status_code
            response_text = error.response.text

            print(f"Search failed: {search_query.name}")
            print(f"GitHub returned HTTP {status_code}")
            print(f"Response: {response_text}")

        except httpx.RequestError as error:
            total_failed_queries += 1

            print(f"Search failed: {search_query.name}")
            print(f"Network error: {error}")
            
        time.sleep(10)

    print("")
    print("Collector run complete.")
    print(f"Saved or updated issues: {total_saved}")
    print(f"Skipped results: {total_skipped}")
    print(f"Failed queries: {total_failed_queries}")


if __name__ == "__main__":
    main()