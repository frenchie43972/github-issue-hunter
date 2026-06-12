export interface GitHubIssue {
  id: number;
  github_issue_id: number;
  github_issue_number: number;
  github_repository_owner: string;
  github_repository_name: string;
  github_repository_full_name: string;
  github_issue_url: string;
  github_repository_url: string;
  title: string;
  body_preview: string | null;
  state: string;
  labels: Array<Record<string, unknown>>;
  is_assigned: boolean;
  assignee_count: number;
  comment_count: number;
  repository_primary_language: string | null;
  repository_stars: number | null;
  repository_forks: number | null;
  repository_open_issues_count: number | null;
  repository_is_archived: boolean | null;
  repository_is_disabled: boolean | null;
  source_query: string;
  collected_by: string;
  collected_at: string;
  github_created_at: string;
  github_updated_at: string;
  github_closed_at: string | null;
}
