# GitHub Issue Collector Agent

The GitHub Issue Collector Agent is the first working collector in the GitHub Issue Hunter project.

Its job is to search GitHub for candidate open-source issues, normalize the raw GitHub API response, and store those issue records in PostgreSQL.

This collector is focused on collection and persistence only. It does not score issues, classify issues, summarize issues with AI, or decide whether an issue is worth attempting.

## Current Collector Flow

```text
GitHub Search Queries
        ↓
GitHub REST API
        ↓
Raw GitHub Issue Data
        ↓
Issue Normalizer
        ↓
Issue Store
        ↓
PostgreSQL github_issues table
```

## Current Capabilities

The collector currently can:

- Load runtime settings from the root `.env` file
- Connect to PostgreSQL using `DATABASE_URL`
- Search GitHub issues using configured search queries
- Fetch public GitHub issue results
- Normalize GitHub API issue data into the internal database shape
- Insert or update records in the `github_issues` table
- Avoid duplicate issue rows using `github_issue_id`
- Continue running when an individual GitHub query fails
- Print a per-query and final run summary

## Directory Structure

```text
collector/
├── README.md
├── requirements.txt
├── pyproject.toml
├── collector/
    └──__pycache__
│   ├── config.py
│   ├── database_check.py
│   ├── github_client.py
│   ├── issue_normalizer.py
│   ├── issue_store.py
│   ├── main.py
│   └── search_queries.py
└── tests/
    └── test_issue_normalizer.py
```

## File Responsibilities

### `config.py`

Loads environment variables from the root `.env` file.

Current settings used by the collector:

- `DATABASE_URL`
- `GITHUB_TOKEN`

`DATABASE_URL` is required.

`GITHUB_TOKEN` may be blank for unauthenticated public GitHub API requests. A real GitHub token should be added later to improve rate limits and reliability.

### `database_check.py`

Small diagnostic script used to verify that Python can connect to PostgreSQL and read from the `github_issues` table.

Run it from the outer `collector/` directory:

```powershell
python -m collector.database_check
```

Expected output:

```text
Database connection successful. github_issues row count: 0
```

The row count may be higher if the collector has already inserted issues.

### `search_queries.py`

Defines the configured GitHub issue search queries.

Each query has:

- `name`
- `query`

The current queries focus on open, unassigned GitHub issues that may be plausible for a newer contributor to inspect.

Current query categories include:

- Good first issue
- Help wanted
- Documentation
- Docs label
- README
- Error messages
- UI / UX
- Bugs

These queries are not intended to be perfect. They provide the first working collection surface. Search quality can be improved later through better query configuration and scoring.

### `github_client.py`

Handles communication with the GitHub REST API.

Responsibilities:

- Build GitHub API request headers
- Include a GitHub token when one is configured
- Search GitHub issues
- Return raw GitHub API issue objects

This file does not normalize data and does not write to the database.

### `issue_normalizer.py`

Converts raw GitHub API issue objects into the internal dictionary shape expected by `issue_store.py` and the `github_issues` table.

Responsibilities:

- Skip pull request results
- Extract repository owner/name information
- Build `body_preview`
- Normalize labels
- Map GitHub fields to database fields

The normalizer is the boundary between external GitHub API data and GitHub Issue Hunter's internal issue record shape.

### `issue_store.py`

Writes normalized GitHub issue records to PostgreSQL.

Responsibilities:

- Insert new GitHub issue records
- Update existing records when `github_issue_id` already exists
- Store labels as PostgreSQL `JSONB`
- Keep `collected_at` updated when a record is refreshed

This file does not call GitHub and does not decide which issues are worth collecting.

### `main.py`

Main collector entry point.

Current flow:

1. Load configured search queries
2. Run each GitHub search
3. Normalize returned issues
4. Save normalized issues to PostgreSQL
5. Print a run summary

Run it from the outer `collector/` directory:

```powershell
python -m collector.main
```

## Environment Requirements

The collector expects the root project `.env` file to contain:

```env
DATABASE_URL=postgresql://github_hunter:github_hunter@127.0.0.1:15432/github_issue_hunter
GITHUB_TOKEN=
```

For local Windows development, PostgreSQL is mapped to host port `15432` to avoid conflicts with other local PostgreSQL services.

The Docker Compose mapping should be:

```yaml
ports:
  - '15432:5432'
```

The container still uses port `5432` internally. The Windows host connects through `15432`.

## Local Setup

From the outer `collector/` directory:

```powershell
py -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet, install the current collector dependencies manually:

```powershell
pip install pydantic-settings "psycopg[binary]" httpx
```

Then create the requirements file:

```powershell
pip freeze > requirements.txt
```

## Running PostgreSQL

From the project root:

```powershell
docker compose up -d
```

Check that the container is running:

```powershell
docker compose ps
```

Expected port mapping:

```text
0.0.0.0:15432->5432/tcp
```

## Creating the Database Table

If the database volume is brand new, Docker's Postgres init behavior should run SQL files mounted into:

```text
/docker-entrypoint-initdb.d
```

If the database volume already exists, init SQL files will not automatically rerun. In that case, apply the SQL manually from the project root:

```powershell
Get-Content .\db\init\001_create_github_issues_table.sql | docker exec -i github-issue-hunter-postgres psql -U github_hunter -d github_issue_hunter
```

Verify the table exists:

```powershell
docker exec -it github-issue-hunter-postgres psql -U github_hunter -d github_issue_hunter
```

Then inside `psql`:

```sql
\dt
```

Expected table:

```text
github_issues
```

Exit `psql`:

```sql
\q
```

## Checking Database Connectivity

From the outer `collector/` directory with `.venv` active:

```powershell
python -m collector.database_check
```

Expected output:

```text
Database connection successful. github_issues row count: 0
```

The row count depends on whether the collector has already inserted records.

## Running the Collector

Make sure Docker/PostgreSQL is running from the project root:

```powershell
docker compose up -d
```

Then from the outer `collector/` directory:

```powershell
python -m collector.main
```

Example output:

```text
GitHub Issue Collector Agent started.

Running search: good_first_issue
Query: is:issue state:open no:assignee label:"good first issue"
Finished search: good_first_issue saved=5 skipped=0

Running search: help_wanted
Query: is:issue state:open no:assignee label:"help wanted"
Finished search: help_wanted saved=5 skipped=0

Collector run complete.
Saved or updated issues: 40
Skipped results: 0
Failed queries: 0
```

## Verifying Collected Issues

Open `psql` inside the Postgres container:

```powershell
docker exec -it github-issue-hunter-postgres psql -U github_hunter -d github_issue_hunter
```

Run:

```sql
SELECT
    id,
    github_repository_full_name,
    title,
    source_query
FROM github_issues
ORDER BY collected_at DESC
LIMIT 10;
```

Exit `psql`:

```sql
\q
```

## Current Database Table

The collector writes to:

```text
github_issues
```

This table stores the canonical GitHub issue record collected from GitHub.

Future scoring, AI review, and decision outputs should be stored in separate tables rather than mixed into this source table.

Possible future tables:

```text
github_issue_scores
github_issue_ai_reviews
collector_runs
```

## Current Limitations

The collector currently does not:

- Score issues
- Classify issues as Look / Maybe / Skip
- Summarize issue bodies with AI
- Fetch full repository details beyond what is available in the issue search response
- Handle pagination beyond the current `per_page` setting
- Store collector run history
- Support non-GitHub bounty platforms
- Run on a schedule

These are intentional future improvements.

## Known Local Development Note

On Windows, local Postgres port conflicts can happen if another PostgreSQL service is already listening on `5432` or if Docker has a stale/conflicted port route.

For this project, local Docker Postgres should use host port `15432`.

Correct root `.env` value:

```env
DATABASE_URL=postgresql://github_hunter:github_hunter@127.0.0.1:15432/github_issue_hunter
```

Correct `docker-compose.yml` port mapping:

```yaml
ports:
  - '15432:5432'
```

This avoids the earlier connection issue where Python appeared to hit the wrong Postgres listener.

## Next Likely Improvements

Recommended next improvements after this collector foundation:

1. Add tests for `issue_normalizer.py`
2. Add a `collector_runs` table for run tracking
3. Improve GitHub query configuration
4. Add basic pagination controls
5. Add repository enrichment for stars, forks, language, archived status, and disabled status
6. Build the FastAPI backend to expose collected issues
7. Build the Nuxt dashboard table

## Project Status

The collector has reached its first working end-to-end milestone:

```text
GitHub REST API → Collector → Normalizer → PostgreSQL
```

This completes the initial GitHub Issue Collector Agent foundation.
