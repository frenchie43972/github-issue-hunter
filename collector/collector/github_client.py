"""GitHub REST API client for the GitHub Issue Collector Agent.

This module is responsible only for communicating with GitHub. It does not
normalize issue data and it does not write to the database.
"""

from typing import Any

import httpx

from collector.config import settings

GITHUB_API_BASE_URL = 'https://api.github.com'

def build_github_headers() -> dict[str, str]:
  """HTTP headers required for GitHub REST API requests.

  GitHub recommends sending the vendor JSON Accept header and the explicit
  API version header for REST API calls. The token is optional for now, but
  authenticated requests have higher rate limits than unauthenticated ones.
  """
  headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'github-issue-hunter-collector',
  }
  
  if settings.github_token and settings.github_token != 'your_github_token_here':
    headers['Authorization'] = f'Bearer {settings.github_token}'
    
  return headers

def search_issues(query: str, per_page: int = 20) -> list[dict[str, Any]]:
  """Search GitHub issues using the GitHub REST API.

  Args:
      query: GitHub issue search query string.
      per_page: Maximum number of results to return for this request.

  Returns a list of raw GitHub issue objects from the API response.

  Raises:
      httpx.HTTPStatusError: If GitHub returns a non-success HTTP status.
      httpx.RequestError: If the network request fails.
  """
  params = {
    'q': query,
    'sort': 'updated',
    'order': 'desc',
    'per_page': per_page,
  } 
  
  with httpx.Client(
    base_url=GITHUB_API_BASE_URL,
    headers=build_github_headers(),
    timeout=20.0,
  ) as client:
    response = client.get('/search/issues', params=params)
    response.raise_for_status()
    
  data = response.json()
  return data.get('items', [])