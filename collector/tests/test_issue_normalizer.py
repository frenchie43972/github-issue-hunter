"""
  Tests for GitHub issue normalization.

  These tests focus on small, predictable functions first. That keeps the test suite easy to understand before full GitHub API payload testing.
"""

from collector.issue_normalizer import (
  MAX_BODY_PREVIEW_LENGTH,
  build_body_preview,
  normalize_github_issue,
  parse_repository_from_api_url,
)

SAMPLE_GITHUB_ISSUE = {
    "id": 123456789,
    "node_id": "I_kwDOExampleNode",
    "number": 42,
    "repository_url": "https://api.github.com/repos/example-owner/example-repo",
    "html_url": "https://github.com/example-owner/example-repo/issues/42",
    "title": "Improve README setup instructions",
    "body": "The README setup steps are missing one required command.",
    "state": "open",
    "labels": [
        {
            "name": "documentation",
            "color": "0075ca",
            "description": "Documentation improvements",
        },
        {
            "name": "good first issue",
            "color": "7057ff",
            "description": "Good for newcomers",
        },
    ],
    "assignees": [],
    "comments": 2,
    "created_at": "2026-06-01T00:00:00Z",
    "updated_at": "2026-06-01T01:00:00Z",
    "closed_at": None,
}

def test_build_body_preview_returns_none_when_body_is_missing() -> None:
  """A missing GitHub issue should stay missing"""
  
  result = build_body_preview(None)
  assert result is None
  
def test_build_body_preview_collapses_extra_whitespace() -> None:
  """Body previews should be compact enough for the dashboard display"""
  
  body = 'This    issue\n\nhas    some    messy spacing'
  
  result = build_body_preview(body)
  
  assert result == 'This issue has some messy spacing'
  
def test_build_body_preview_truncates_long_body() -> None:
  """Long issue bodies should be shortened for the preview display."""
  
  body = 'a' * (MAX_BODY_PREVIEW_LENGTH + 50)
  
  result = build_body_preview(body)
  
  assert result is not None
  assert len(result) == MAX_BODY_PREVIEW_LENGTH 
  assert result.endswith('...')
  
def test_parse_repository_from_api_url_returns_owner_name_and_full_name() -> None:
  """Repository API URLs should be converted into owner/repo parts."""
  
  repository_url = 'https://api.github.com/repos/example-owner/example-repo'
  
  owner, repository_name, repository_full_name = parse_repository_from_api_url(
    repository_url
  )
  
  assert owner == 'example-owner'
  assert repository_name == 'example-repo'
  assert repository_full_name == 'example-owner/example-repo'
  
def test_normalize_github_issue_returns_database_ready_payload() -> None:
    """
    A raw GitHub issue should normalize into the database payload shape.
    
    """

    result = normalize_github_issue(
        raw_issue=SAMPLE_GITHUB_ISSUE,
        source_query='is:issue state:open no:assignee label:"good first issue"',
    )

    assert result is not None
    assert result["github_issue_id"] == 123456789
    assert result["github_node_id"] == "I_kwDOExampleNode"
    assert result["github_issue_number"] == 42
    assert result["github_repository_owner"] == "example-owner"
    assert result["github_repository_name"] == "example-repo"
    assert result["github_repository_full_name"] == "example-owner/example-repo"
    assert result["github_issue_url"] == "https://github.com/example-owner/example-repo/issues/42"
    assert result["github_repository_url"] == "https://github.com/example-owner/example-repo"
    assert result["title"] == "Improve README setup instructions"
    assert result["state"] == "open"
    assert result["is_assigned"] is False
    assert result["assignee_count"] == 0
    assert result["comment_count"] == 2
    assert result["labels"][0]["name"] == "documentation"
    assert result["source_query"] == 'is:issue state:open no:assignee label:"good first issue"'
    assert result["collected_by"] == "github_issue_collector"
    assert result["github_created_at"] == "2026-06-01T00:00:00Z"
    assert result["github_updated_at"] == "2026-06-01T01:00:00Z"
    assert result["github_closed_at"] is None
    
def test_normalize_github_issue_skips_pull_request_results() -> None:
    """Pull request results should not be stored as GitHub issues."""

    pull_request_result = {
        **SAMPLE_GITHUB_ISSUE,
        "pull_request": {
            "url": "https://api.github.com/repos/example-owner/example-repo/pulls/42",
            "html_url": "https://github.com/example-owner/example-repo/pull/42",
        },
    }

    result = normalize_github_issue(
        raw_issue=pull_request_result,
        source_query='is:issue state:open no:assignee label:"good first issue"',
    )

    assert result is None