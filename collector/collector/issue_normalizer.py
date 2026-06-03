"""Normalize raw GitHub API issue data.

This module converts GitHub's raw REST API response objects into the internal
dictionary shape expected by issue_store.py and the github_issues table.
"""

from typing import Any

MAX_BODY_PREVIEW_LENGTH = 300

def build_body_preview(body: str | None) -> str | None:
  """
    Args:
      body: Raw GitHub issue body text.

    Returns:
      A trimmed preview string, or None when the issue has no body.
  """
  
  if not body:
    return None
  
  normalized_body = ' '.join(body.split())
  
  if len(normalized_body) <= MAX_BODY_PREVIEW_LENGTH:
    return normalized_body
  
  return f'{normalized_body[:MAX_BODY_PREVIEW_LENGTH].rstrip()}'

def parse_repository_from_api_url(repository_url: str) -> tuple[str, str, str]:
  """
    Extract repository owner/name values from GitHub's API repository URL.

    GitHub issue search results include repository_url in this format:
      https://api.github.com/repos/{owner}/{repo}

    Args:
      repository_url: GitHub API repository URL from the issue payload.

    Returns:
      A tuple containing owner, repo name, and owner/repo full name.
  """
  
  prefix = 'https://api.github.com/repos/'
  repository_full_name = repository_url.removeprefix(prefix)
  
  owner, repository_name  = repository_full_name.split('/', maxsplit=1)
  
  return owner, repository_name, repository_full_name

def normalize_github_issue(
  raw_issue: dict[str, Any],
  source_query: str,
  collected_by: str = 'github_issue_collector'
) -> dict[str, Any] | None:
  """
    Convert one raw GitHub issue object into the database payload shape.

    Args:
      raw_issue: One issue object returned by the GitHub REST API.
      source_query: The GitHub search query that returned this issue.
      collected_by: Name of the collector process producing the record.

    Returns:
      A normalized issue dictionary ready for issue_store.py, or None if the
      API object is a pull request instead of a true issue.
  """
  
  if 'pull_request' in raw_issue:
    return None
  
  owner, repository_name, repository_full_name = parse_repository_from_api_url(
    raw_issue['repository_url']
  )
  
  assignees = raw_issue.get("assignees") or []
  
  labels = [
    {
      'name': label.get('name'),
      'color': label.get('color'),
      'description': label.get('description'),
    }
    for label in raw_issue.get('labels', [])
  ]
  
  return {
    "github_issue_id": raw_issue["id"],
    "github_node_id": raw_issue.get("node_id"),
    "github_issue_number": raw_issue["number"],
    "github_repository_owner": owner,
    "github_repository_name": repository_name,
    "github_repository_full_name": repository_full_name,
    "github_repository_id": None,
    "github_issue_url": raw_issue["html_url"],
    "github_repository_url": f"https://github.com/{repository_full_name}",
    "title": raw_issue["title"],
    "body": raw_issue.get("body"),
    "body_preview": build_body_preview(raw_issue.get("body")),
    "state": raw_issue.get("state", "open"),
    "labels": labels,
    "is_assigned": len(assignees) > 0,
    "assignee_count": len(assignees),
    "comment_count": raw_issue.get("comments", 0),
    "repository_primary_language": None,
    "repository_stars": None,
    "repository_forks": None,
    "repository_open_issues_count": None,
    "repository_is_archived": None,
    "repository_is_disabled": None,
    "source_query": source_query,
    "collected_by": collected_by,
    "github_created_at": raw_issue["created_at"],
    "github_updated_at": raw_issue["updated_at"],
    "github_closed_at": raw_issue.get("closed_at"),
  }