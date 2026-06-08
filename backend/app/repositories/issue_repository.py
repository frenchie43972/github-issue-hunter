"""Database queries for collected GitHub issues.

The repository layer owns SQL for reading issue records from PostgreSQL.
FastAPI routes should call this layer instead of embedding SQL directly in
route functions.
"""

from typing import Any

import psycopg
from psycopg.rows import dict_row

from app.config import settings


def list_github_issues(limit: int = 50) -> list[dict[str, Any]]:
    """Return recently collected GitHub issues.

    Args:
        limit: Maximum number of issue records to return.

    Returns:
        A list of dictionaries, where each dictionary represents one row from github_issues table.
    """

    sql = """
        SELECT
            id,
            github_issue_id,
            github_issue_number,
            github_repository_owner,
            github_repository_name,
            github_repository_full_name,
            github_issue_url,
            github_repository_url,
            title,
            body_preview,
            state,
            labels,
            is_assigned,
            assignee_count,
            comment_count,
            repository_primary_language,
            repository_stars,
            repository_forks,
            repository_open_issues_count,
            repository_is_archived,
            repository_is_disabled,
            source_query,
            collected_by,
            collected_at,
            github_created_at,
            github_updated_at,
            github_closed_at
        FROM github_issues
        ORDER BY collected_at DESC
        LIMIT %(limit)s;
    """

    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"limit": limit})
            rows = cur.fetchall()

    return list(rows)