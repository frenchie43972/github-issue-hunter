"""Database write operations for GitHub issue records.

This module is responsible for saving normalized GitHub issue data into
PostgreSQL. It does not call the GitHub API and it does not decide which
issues are worth collecting. Its job is only persistence.
"""

from typing import Any

import psycopg # type: ignore
from psycopg.types.json import Jsonb # type: ignore

from collector.config import settings

def upsert_github_issue(issue: dict[str, Any]) -> None:
  """Insert or update one GitHub issue record.

    The collector may encounter the same issue across multiple runs. Instead
    of inserting duplicates, this function uses GitHub's issue ID as the
    conflict target and refreshes the existing row when needed.
    """
  sql = """
        INSERT INTO github_issues (
            github_issue_id,
            github_node_id,
            github_issue_number,
            github_repository_owner,
            github_repository_name,
            github_repository_full_name,
            github_repository_id,
            github_issue_url,
            github_repository_url,
            title,
            body,
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
            github_created_at,
            github_updated_at,
            github_closed_at
        )
        VALUES (
            %(github_issue_id)s,
            %(github_node_id)s,
            %(github_issue_number)s,
            %(github_repository_owner)s,
            %(github_repository_name)s,
            %(github_repository_full_name)s,
            %(github_repository_id)s,
            %(github_issue_url)s,
            %(github_repository_url)s,
            %(title)s,
            %(body)s,
            %(body_preview)s,
            %(state)s,
            %(labels)s,
            %(is_assigned)s,
            %(assignee_count)s,
            %(comment_count)s,
            %(repository_primary_language)s,
            %(repository_stars)s,
            %(repository_forks)s,
            %(repository_open_issues_count)s,
            %(repository_is_archived)s,
            %(repository_is_disabled)s,
            %(source_query)s,
            %(collected_by)s,
            %(github_created_at)s,
            %(github_updated_at)s,
            %(github_closed_at)s
        )
        ON CONFLICT (github_issue_id)
        DO UPDATE SET
            github_node_id = EXCLUDED.github_node_id,
            github_issue_number = EXCLUDED.github_issue_number,
            github_repository_owner = EXCLUDED.github_repository_owner,
            github_repository_name = EXCLUDED.github_repository_name,
            github_repository_full_name = EXCLUDED.github_repository_full_name,
            github_repository_id = EXCLUDED.github_repository_id,
            github_issue_url = EXCLUDED.github_issue_url,
            github_repository_url = EXCLUDED.github_repository_url,
            title = EXCLUDED.title,
            body = EXCLUDED.body,
            body_preview = EXCLUDED.body_preview,
            state = EXCLUDED.state,
            labels = EXCLUDED.labels,
            is_assigned = EXCLUDED.is_assigned,
            assignee_count = EXCLUDED.assignee_count,
            comment_count = EXCLUDED.comment_count,
            repository_primary_language = EXCLUDED.repository_primary_language,
            repository_stars = EXCLUDED.repository_stars,
            repository_forks = EXCLUDED.repository_forks,
            repository_open_issues_count = EXCLUDED.repository_open_issues_count,
            repository_is_archived = EXCLUDED.repository_is_archived,
            repository_is_disabled = EXCLUDED.repository_is_disabled,
            source_query = EXCLUDED.source_query,
            collected_by = EXCLUDED.collected_by,
            collected_at = NOW(),
            github_created_at = EXCLUDED.github_created_at,
            github_updated_at = EXCLUDED.github_updated_at,
            github_closed_at = EXCLUDED.github_closed_at;
    """
  
  payload = issue.copy()
  
  # Convert Python list/dict label data into a PostgreSQL JSONB value.
  # This keeps JSON handling explicit at the database boundary.
  payload['labels'] = Jsonb(payload['labels'])
  
  # Open a database connection using the DATABASE_URL loaded from .env.
  # The connection and cursor are automatically closed after the block exits.
  with psycopg.connect(settings.database_url) as conn:
    with conn.cursor() as cur:
      cur.execute(sql, payload)