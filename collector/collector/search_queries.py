"""GitHub issue search query configuration.

This module defines the first search queries used by the GitHub Issue
Collector Agent.

The collector will pass these query strings to GitHub's issue search API.
Each query is intentionally focused on open, unassigned issues that may be
reasonable for a newer contributor to inspect.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class GitHubIssueSearchQuery:
  """
      name: Internal name used in logs and debugging.
      query: GitHub issue search syntax sent to the GitHub API.
  """
  name: str
  query: str
  
SEARCH_QUERIES: list[GitHubIssueSearchQuery] = [
  GitHubIssueSearchQuery(
    name='good_first_issue',
    query='is:issue state:open no:assignee label:"good first issue"',
  ),
  GitHubIssueSearchQuery(
        name="help_wanted",
        query='is:issue state:open no:assignee label:"help wanted"',
  ),
  GitHubIssueSearchQuery(
      name="documentation",
      query='is:issue state:open no:assignee documentation',
  ),
  GitHubIssueSearchQuery(
      name="docs_label",
      query='is:issue state:open no:assignee label:"docs"',
  ),
  GitHubIssueSearchQuery(
      name="readme",
      query='is:issue state:open no:assignee README',
  ),
  GitHubIssueSearchQuery(
      name="error_message",
      query='is:issue state:open no:assignee "error message"',
  ),
  GitHubIssueSearchQuery(
      name="ui_ux",
      query='is:issue state:open no:assignee UI UX',
  ),
  GitHubIssueSearchQuery(
        name="small_bug",
        query='is:issue state:open no:assignee bug',
  ),
]