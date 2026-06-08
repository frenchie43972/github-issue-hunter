"""API routes for collected GitHub issues."""

from fastapi import APIRouter, Query

from app.repositories.issue_repository import list_github_issues
from app.schemas.issue import GitHubIssueResponse

router = APIRouter(
  prefix='/issues',
  tags=['issues'],
)

@router.get('', response_model=list[GitHubIssueResponse])
def get_issues(
  limit: int = Query(default=50, ge=1, le=100)
) -> list[GitHubIssueResponse]:
  """Return recently collected GitHub issues.

    Args:
        limit: Maximum number of issues to return. The API caps this at 100
            so a single request cannot accidentally return too much data.

    Returns:
        A list of collected GitHub issues ordered by most recently collected.
  """
  issues = list_github_issues(limit=limit)
  
  return [GitHubIssueResponse.model_validate(issue) for issue in issues]