"""API response schemas.

Schemas define the shape of data returned by the FastAPI backend. They keep
the API response predictable for the Nuxt frontend and for tools like Postman.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class GitHubIssueResponse(BaseModel):
    """Public API representation of a collected GitHub issue."""

    id: int
    github_issue_id: int
    github_issue_number: int

    github_repository_owner: str
    github_repository_name: str
    github_repository_full_name: str

    github_issue_url: str
    github_repository_url: str

    title: str
    body_preview: str | None
    state: str
    labels: list[dict[str, Any]]

    is_assigned: bool
    assignee_count: int
    comment_count: int

    repository_primary_language: str | None
    repository_stars: int | None
    repository_forks: int | None
    repository_open_issues_count: int | None
    repository_is_archived: bool | None
    repository_is_disabled: bool | None

    source_query: str
    collected_by: str
    collected_at: datetime

    github_created_at: datetime
    github_updated_at: datetime
    github_closed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)