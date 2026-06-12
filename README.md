# GitHub Issue Hunter

GitHub Issue Hunter is a browser-based local development project that collects real open-source GitHub issues, stores them in PostgreSQL, exposes them through a FastAPI backend, and displays them in a Nuxt dashboard.

The project originally began under the working name **GitHub Issue Radar**. It was later renamed to **GitHub Issue Hunter**.

Repository name:

```text
github-issue-hunter
```

This is a real learning/build project. It should continue to be developed incrementally, using current documentation, small working steps, and restrained architecture.

---

## Project Purpose

The purpose of GitHub Issue Hunter is to reduce the noise involved in manually searching GitHub for possible open-source contributions.

The application is intended to help answer:

> Which GitHub issues are worth my attention today?

The user is especially interested in contained, beginner-plausible work such as:

- Documentation changes
- README improvements
- Small UI or UX behavior fixes
- Visual or aesthetic polish
- Obvious bugs
- Better error messages
- Small scripts or automation
- Configuration fixes
- Other clearly scoped contributions

The issues displayed by the application are real, live GitHub issues from real repositories. They are not dummy data.

---

## Long-Term Direction

The long-term goal is to evolve the project into a transparent multi-agent decision system.

Possible future agents include:

- GitHub Issue Collector Agent
- Normalizer Agent
- Rule-Based Scoring Agent
- AI Review or Reasoning Agent
- Dashboard or Reporting Agent
- Later, collectors for other open-source or bounty platforms

The project should not jump directly into a complex multi-agent framework.

The intended foundation is:

```text
GitHub API
   ↓
Python Collector Agent
   ↓
PostgreSQL
   ↓
FastAPI Backend
   ↓
Nuxt Dashboard
```

The GitHub Issue Collector is the first agent. It does not currently use an AI API.

---

## Original Phase 1 Goal

Phase 1 was intended to create a working local vertical slice that could:

1. Query GitHub issues through the GitHub API.
2. Store issue results in PostgreSQL.
3. Expose stored issues through a FastAPI backend.
4. Display stored issues in a Nuxt browser dashboard.
5. Let the user inspect candidate issues without manually searching GitHub.

That vertical slice is now working.

---

## Original Phase 1 Non-Goals

The following were intentionally excluded from Phase 1:

- User accounts
- Authentication for application users
- Payments
- Hosting or deployment
- AI API integration
- Vector databases
- Background job queues
- Redis
- Multi-user support
- Complex agent frameworks
- Full commercial product structure
- Support for non-GitHub platforms
- Excessive UI polish
- Premature abstractions

These should remain out of scope unless a later phase explicitly introduces them.

---

## Development Principles

Continue the project using these rules:

- Work one clear step at a time.
- Prefer small working increments.
- Confirm the current step works before moving ahead.
- Use current official documentation for version-sensitive guidance.
- Do not provide legacy Nuxt, FastAPI, PostgreSQL, Docker, or package guidance.
- Do not overbuild.
- Do not introduce commercial features prematurely.
- Explain commands and why they are being run.
- State which files are being changed and why.
- Avoid changing working code based on guesses.
- Inspect the actual existing code before proposing edits.
- Restart affected development servers after dependency, environment, or configuration changes before diagnosing application code.
- Do not move ahead without confirming the current step works.
- Treat the project as a professional application developed incrementally, not as a disposable prototype.

---

## Technology Stack

### Frontend

- Nuxt 4
- Vue 3
- TypeScript
- Nuxt UI 4
- Tailwind CSS through the current Nuxt UI setup

### Backend

- Python
- FastAPI
- Pydantic
- pydantic-settings
- psycopg

### Collector

- Python
- httpx
- pydantic-settings
- psycopg
- pytest

### Database

- PostgreSQL 18
- Docker Compose

### Local Development

- Root `.env` file
- Separate Python virtual environments for the backend and collector
- Nuxt development server
- FastAPI development server
- Dockerized PostgreSQL

### External Data Source

- GitHub REST API
- GitHub personal access token when configured
- No GitHub HTML scraping

---

## Current Project Structure

```text
github-issue-hunter/
├── README.md
├── .gitignore
├── .env
├── .env.example
├── docker-compose.yml
├── frontend/
│   ├── package.json
│   ├── nuxt.config.ts
│   ├── tsconfig.json
│   ├── app/
│   │   ├── app.vue
│   │   ├── assets/
│   │   │   └── css/
│   │   │       └── main.css
│   │   ├── pages/
│   │   │   └── index.vue
│   │   ├── components/
│   │   │   ├── IssueCard.vue
│   │   │   ├── IssueGrid.vue
│   │   │   └── IssueTable.vue
│   │   └── types/
│   │       └── issue.ts
│   └── README.md
├── backend/
│   ├── pyproject.toml
│   ├── README.md
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   └── issue.py
│   │   ├── schemas/
│   │   │   └── issue.py
│   │   ├── repositories/
│   │   │   └── issue_repository.py
│   │   └── routers/
│   │       └── issues.py
│   └── tests/
│       └── test_health.py
├── collector/
│   ├── pyproject.toml
│   ├── README.md
│   ├── requirements.txt
│   ├── collector/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database_check.py
│   │   ├── github_client.py
│   │   ├── issue_normalizer.py
│   │   ├── issue_store.py
│   │   └── search_queries.py
│   └── tests/
│       └── test_issue_normalizer.py
└── db/
    ├── init/
    │   └── 001_create_github_issues_table.sql
    └── README.md
```

`IssueTable.vue` has effectively been replaced by the card/grid approach and can be removed once it is confirmed no longer referenced.

---

## Environment Configuration

The root `.env` currently follows this structure:

```env
GITHUB_TOKEN=
DATABASE_URL=postgresql://github_hunter:github_hunter@127.0.0.1:15432/github_issue_hunter

POSTGRES_DB=github_issue_hunter
POSTGRES_USER=github_hunter
POSTGRES_PASSWORD=github_hunter

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

The real GitHub token belongs only in `.env`.

Example:

```env
GITHUB_TOKEN=your_real_token_here
```

Do not hardcode the token in Python source files.

The root `.env` must remain excluded by `.gitignore`.

---

## PostgreSQL and Docker Configuration

The local PostgreSQL container uses host port `15432`.

This avoids Windows host-port conflicts that previously occurred on ports `5432` and `5433`.

The application database URL is:

```text
postgresql://github_hunter:github_hunter@127.0.0.1:15432/github_issue_hunter
```

Current Docker Compose configuration:

```yaml
services:
  postgres:
    image: postgres:18.4
    container_name: github-issue-hunter-postgres
    restart: unless-stopped
    ports:
      - '15432:5432'
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - github_issue_hunter_postgres_data:/var/lib/postgresql
      - ./db/init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  github_issue_hunter_postgres_data:
```

Important PostgreSQL 18 detail:

```text
/var/lib/postgresql
```

is the correct persistent volume target for the official PostgreSQL 18 image used here.

Do not change it back to:

```text
/var/lib/postgresql/data
```

The earlier database connection problem was caused by a Windows host-port conflict or stale host route, not by incorrect PostgreSQL credentials or schema.

---

## Database Initialization

The schema file is:

```text
db/init/001_create_github_issues_table.sql
```

The primary table is:

```text
github_issues
```

On a new computer or a fresh Docker volume, the table may need to be applied manually.

From the project root in PowerShell:

```powershell
Get-Content .\db\init\001_create_github_issues_table.sql |
  docker exec -i github-issue-hunter-postgres `
  psql -U github_hunter -d github_issue_hunter
```

This command:

1. Reads the SQL initialization file.
2. Pipes the SQL into the running PostgreSQL container.
3. Executes it against the `github_issue_hunter` database.

To enter PostgreSQL manually:

```powershell
docker exec -it github-issue-hunter-postgres `
  psql -U github_hunter -d github_issue_hunter
```

Exit `psql` with:

```text
\q
```

Exit the PostgreSQL pager with:

```text
q
```

---

## Database Schema

The `github_issues` table currently stores:

- `id`
- `github_issue_id`
- `github_node_id`
- `github_issue_number`
- `github_repository_owner`
- `github_repository_name`
- `github_repository_full_name`
- `github_repository_id`
- `github_issue_url`
- `github_repository_url`
- `title`
- `body`
- `body_preview`
- `state`
- `labels`
- `is_assigned`
- `assignee_count`
- `comment_count`
- `repository_primary_language`
- `repository_stars`
- `repository_forks`
- `repository_open_issues_count`
- `repository_is_archived`
- `repository_is_disabled`
- `source_query`
- `collected_by`
- `collected_at`
- `github_created_at`
- `github_updated_at`
- `github_closed_at`

The primary key uses:

```sql
BIGINT GENERATED ALWAYS AS IDENTITY
```

Labels are stored as:

```sql
JSONB NOT NULL DEFAULT '[]'::jsonb
```

Current uniqueness constraints include:

- `github_issue_id`
- `github_issue_url`

Current validation constraints include:

- Nonnegative assignee counts
- Nonnegative comment counts
- Nonnegative star counts
- Nonnegative fork counts
- Issue state restricted to `open` or `closed`

Current indexes include:

- `idx_github_issues_collected_at`
- `idx_github_issues_github_updated_at`
- `idx_github_issues_repository_full_name`
- `idx_github_issues_source_query`
- `idx_github_issues_is_assigned`
- `idx_github_issues_repository_primary_language`
- `idx_github_issues_state`
- `idx_github_issues_labels_gin`

---

## Collector

The collector is the first agent in the future multi-agent system.

Current flow:

```text
GitHub API
   ↓
github_client.py
   ↓
issue_normalizer.py
   ↓
issue_store.py
   ↓
PostgreSQL
```

The collector is run from the outer `collector/` directory.

The outer collector directory has its own virtual environment.

Typical activation command:

```powershell
.\.venv\Scripts\activate
```

Run the collector with:

```powershell
python -m collector.main
```

Do not run it from inside:

```text
collector/collector/
```

Run it from the outer:

```text
collector/
```

---

## Collector Configuration

File:

```text
collector/collector/config.py
```

The collector loads the root `.env` file using `pydantic-settings`.

The project root is resolved with:

```python
PROJECT_ROOT = Path(__file__).resolve().parents[2]
```

Important settings include:

- `DATABASE_URL`
- `GITHUB_TOKEN`

---

## GitHub Client

File:

```text
collector/collector/github_client.py
```

The GitHub API base URL is:

```python
GITHUB_API_BASE_URL = 'https://api.github.com'
```

The client sends these headers:

- `Accept: application/vnd.github+json`
- GitHub API version header
- A project-specific `User-Agent`
- `Authorization: Bearer ...` when a valid token is configured

The current token check is similar to:

```python
if settings.github_token and settings.github_token != 'your_github_token_here':
    headers['Authorization'] = f'Bearer {settings.github_token}'
```

The real token remains in `.env`.

The collector currently uses the real GitHub Search API.

The results are not fixtures or dummy data.

---

## Current GitHub Search Queries

File:

```text
collector/collector/search_queries.py
```

Current search definitions include:

```text
good_first_issue
is:issue state:open no:assignee label:"good first issue"
```

```text
help_wanted
is:issue state:open no:assignee label:"help wanted"
```

```text
documentation
is:issue state:open no:assignee documentation
```

```text
docs_label
is:issue state:open no:assignee label:"docs"
```

```text
readme
is:issue state:open no:assignee README
```

```text
error_message
is:issue state:open no:assignee "error message"
```

```text
ui_ux
is:issue state:open no:assignee UI UX
```

```text
small_bug
is:issue state:open no:assignee bug
```

These queries are functional starting points, not final production search strategy.

Some queries are broad and may produce noisy results.

The product goal is still broad discovery. The query list should not be permanently reduced merely because rate limiting occurred. The collector should instead be improved to process the intended searches responsibly.

---

## Issue Normalization

File:

```text
collector/collector/issue_normalizer.py
```

The normalizer converts GitHub API issue objects into the database payload expected by `github_issues`.

Pull requests returned through GitHub’s issue search are skipped by checking for the `pull_request` key.

The body preview length is capped at 300 characters.

Current preview behavior:

```python
MAX_BODY_PREVIEW_LENGTH = 300

def build_body_preview(body: str | None) -> str | None:
    if not body:
        return None

    normalized_body = " ".join(body.split())

    if len(normalized_body) <= MAX_BODY_PREVIEW_LENGTH:
        return normalized_body

    preview_text = normalized_body[
        : MAX_BODY_PREVIEW_LENGTH - 3
    ].rstrip()

    return f"{preview_text}..."
```

Repository ownership is currently parsed from GitHub’s repository API URL.

Repository enrichment fields currently remain nullable until enrichment is implemented.

Examples include:

- Primary language
- Stars
- Forks
- Open issue count
- Archived status
- Disabled status

---

## Issue Storage

File:

```text
collector/collector/issue_store.py
```

The collector inserts or updates issues using:

```sql
ON CONFLICT (github_issue_id) DO UPDATE
```

Labels are converted to PostgreSQL JSONB using psycopg’s JSON support.

This allows the collector to update previously seen issues instead of creating duplicate rows.

---

## Collector Tests

Test file:

```text
collector/tests/test_issue_normalizer.py
```

Current tests cover:

- `None` body previews
- Whitespace normalization
- Long body truncation
- Maximum preview length
- Repository owner/name parsing
- Full issue normalization
- Pull request result skipping

The collector test configuration is in:

```text
collector/pyproject.toml
```

Relevant pytest configuration:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

Run collector tests from the outer `collector/` directory:

```powershell
pytest
```

---

## Backend

The FastAPI backend reads stored issues from PostgreSQL and exposes them to the frontend.

Current backend flow:

```text
PostgreSQL
   ↓
issue_repository.py
   ↓
issues.py router
   ↓
FastAPI
   ↓
GET /issues
```

The backend has its own virtual environment inside:

```text
backend/.venv
```

Activate it from the outer `backend/` directory:

```powershell
.\.venv\Scripts\activate
```

Run FastAPI from the outer `backend/` directory:

```powershell
fastapi dev app/main.py
```

Important:

```text
app/main.py
```

uses a slash.

Do not use:

```text
app.main.py
```

---

## Backend Endpoints

### Health Check

```http
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Database Health Check

```http
GET /health/db
```

Expected response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

### Issue List

```http
GET /issues
```

Optional limit:

```http
GET /issues?limit=25
```

The current limit validation allows values from 1 through 100.

A value such as:

```http
GET /issues?limit=101
```

should return a validation error.

The issue endpoint has been successfully tested in both a browser and Postman.

---

## Backend Files

### Application Entry Point

```text
backend/app/main.py
```

Responsibilities:

- Creates the FastAPI application
- Adds CORS middleware
- Registers the issue router
- Exposes health endpoints

### Database Check

```text
backend/app/database.py
```

Uses psycopg to execute:

```sql
SELECT 1
```

### Response Schema

```text
backend/app/schemas/issue.py
```

Uses a Pydantic `GitHubIssueResponse` model.

The response excludes the full issue body from the dashboard list response and includes `body_preview`.

### Repository Layer

```text
backend/app/repositories/issue_repository.py
```

Reads issues using psycopg with dictionary rows.

Results are ordered by:

```sql
collected_at DESC
```

### Issue Router

```text
backend/app/routers/issues.py
```

The endpoint returns:

```python
list[GitHubIssueResponse]
```

---

## CORS Configuration

The FastAPI backend currently allows these local frontend origins:

```text
http://localhost:3000
http://127.0.0.1:3000
http://localhost:3001
http://127.0.0.1:3001
```

Only `GET` methods are currently allowed.

This is appropriate for the current read-only frontend.

---

## Frontend

The frontend uses Nuxt 4, Vue 3, TypeScript, Nuxt UI, and Tailwind utilities.

Current frontend flow:

```text
GET /issues
   ↓
pages/index.vue
   ↓
IssueGrid.vue
   ↓
IssueCard.vue
```

Run the frontend from:

```text
frontend/
```

Command:

```powershell
npm run dev
```

Expected local URL:

```text
http://localhost:3000/
```

The Nuxt process remains running in the terminal. This is normal and does not mean it is hanging.

---

## Nuxt Configuration

File:

```text
frontend/nuxt.config.ts
```

Current intended configuration:

```ts
import { defineNuxtConfig } from 'nuxt/config';

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: ['@nuxt/eslint', '@nuxt/ui'],

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: 'http://127.0.0.1:8000',
    },
  },
});
```

Do not add:

```text
@nuxtjs/tailwindcss
```

to the modules list.

That older module path was accidentally mixed into the Nuxt UI 4 setup and caused unnecessary PostCSS and configuration problems.

The current setup uses Nuxt UI 4 with Tailwind CSS directly.

---

## Frontend CSS

File:

```text
frontend/app/assets/css/main.css
```

Current imports:

```css
@import 'tailwindcss';
@import '@nuxt/ui';
```

---

## Frontend Application Shell

File:

```text
frontend/app/app.vue
```

Current content:

```vue
<template>
  <NuxtPage />
</template>
```

This is required so Nuxt renders:

```text
frontend/app/pages/index.vue
```

---

## Frontend Type Definition

File:

```text
frontend/app/types/issue.ts
```

Current interface shape:

```ts
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
```

---

## Dashboard Page

File:

```text
frontend/app/pages/index.vue
```

The page:

1. Reads the backend API base URL from Nuxt runtime configuration.
2. Calls the FastAPI `/issues` endpoint.
3. Requests 25 issues.
4. Displays loading and error states.
5. Passes the issue list to `IssueGrid`.

Current fetch pattern:

```vue
<script setup lang="ts">
import type { GitHubIssue } from '~/types/issue';

const config = useRuntimeConfig();

const {
  data: issues,
  status,
  error,
} = await useFetch<GitHubIssue[]>(`${config.public.apiBase}/issues`, {
  query: {
    limit: 25,
  },
  default: () => [],
});
</script>
```

Do not add:

```ts
server: false;
```

The earlier frontend problem was caused by stale development server and browser state after dependency and configuration changes.

Adding `server: false` created a server/client hydration mismatch and was removed.

The normal server-rendered `useFetch` behavior currently works.

Current template structure:

```vue
<template>
  <main class="min-h-screen bg-gray-50 p-6">
    <section class="mx-auto max-w-5xl space-y-6">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">GitHub Issue Hunter</h1>

        <p class="mt-2 text-gray-600">
          Candidate GitHub issues collected for review.
        </p>
      </div>

      <div
        v-if="status === 'pending'"
        class="rounded-lg border border-gray-200 bg-white p-4 text-gray-600"
      >
        Loading issues...
      </div>

      <div
        v-else-if="error"
        class="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700"
      >
        Failed to load issues.
      </div>

      <IssueGrid v-else :issues="issues ?? []" />
    </section>
  </main>
</template>
```

The maximum page width may later be increased to `max-w-7xl` if more horizontal card space is desired.

---

## Issue Grid

File:

```text
frontend/app/components/IssueGrid.vue
```

The issue grid displays responsive cards.

Current intended layout:

```vue
<script setup lang="ts">
import type { GitHubIssue } from '~/types/issue';

defineProps<{
  issues: GitHubIssue[];
}>();
</script>

<template>
  <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    <IssueCard v-for="issue in issues" :key="issue.id" :issue="issue" />
  </div>
</template>
```

Responsive behavior:

- One card per row on very small screens
- Two cards per row on small screens
- Three cards per row on large screens
- Four cards per row on extra-large screens

---

## Issue Card

File:

```text
frontend/app/components/IssueCard.vue
```

Each card displays:

- Issue title
- GitHub issue link
- Repository name
- Repository link
- Issue body preview
- Comment count
- Updated date
- Assignment status
- Labels
- Source query

The card includes helper functions for:

- Formatting dates
- Extracting label names from JSON-shaped label objects

The card and grid are currently working and render real stored GitHub issues.

---

## Frontend Troubleshooting Lessons

Several frontend issues occurred after changing dependencies and Nuxt configuration.

The actual recovery was:

1. Remove the incompatible `@nuxtjs/tailwindcss` module.
2. Keep `@nuxt/ui`.
3. Install or retain the current `tailwindcss` dependency.
4. Regenerate Nuxt types when necessary.
5. Restart the frontend and backend.
6. Open a fresh browser session.

Useful commands:

```powershell
npx nuxi prepare
```

This regenerates Nuxt’s generated TypeScript configuration and auto-import types.

If VS Code still shows stale type errors:

```text
Ctrl + Shift + P
TypeScript: Restart TS Server
```

The following errors can indicate missing or stale Nuxt-generated types:

```text
Cannot find name 'useFetch'
Cannot find name 'useRuntimeConfig'
Cannot find name 'defineNuxtConfig'
```

Do not immediately rewrite working application code when these appear.

First confirm:

- `npm install` completed
- `.nuxt` was regenerated
- `tsconfig.json` extends Nuxt’s generated configuration
- VS Code’s TypeScript server was restarted
- Nuxt was restarted

---

## Browser Console Notes

Warnings from files such as:

```text
contentscript.js
```

including messages about:

- `MaxListenersExceededWarning`
- `ObjectMultiplex`
- orphaned streams
- malformed chunks

are likely caused by a browser extension and not by GitHub Issue Hunter.

The Vue message:

```text
<Suspense> is an experimental feature
```

is normal development output in this context.

A hydration mismatch did occur when `server: false` was added to `useFetch`.

Removing `server: false` resolved it.

---

## Current End-to-End Status

The following full path is working:

```text
Real GitHub API
   ↓
Python collector
   ↓
Issue normalization
   ↓
PostgreSQL
   ↓
FastAPI /issues endpoint
   ↓
Nuxt useFetch
   ↓
Responsive issue cards
```

Confirmed working items:

- PostgreSQL container starts
- Database schema exists
- Collector connects to PostgreSQL
- Collector queries the real GitHub API
- Collector normalizes issues
- Collector upserts issues
- Collector tests pass
- FastAPI health endpoint works
- FastAPI database health endpoint works
- FastAPI issue endpoint works
- Postman can retrieve issues
- Browser can retrieve backend JSON
- Nuxt fetches stored issues
- Issue cards render in a responsive grid
- GitHub issue and repository links are displayed
- GitHub token is being read from `.env`

---

## Current GitHub Rate-Limit Issue

The most recent collector work exposed GitHub secondary rate limits.

Example response:

```json
{
  "documentation_url": "https://docs.github.com/free-pro-team@latest/rest/overview/rate-limits-for-the-rest-api#about-secondary-rate-limits",
  "message": "You have exceeded a secondary rate limit. Please wait a few minutes before you try again."
}
```

This is not necessarily the normal hourly primary rate limit.

It is GitHub’s protection against request patterns that are too rapid, repetitive, or expensive.

The collector currently runs multiple search queries sequentially.

A delay of approximately 10 seconds between searches was tested.

Results improved from:

```text
Saved or updated issues: 10
Failed queries: 6
```

to:

```text
Saved or updated issues: 20
Failed queries: 4
```

However, secondary rate-limit responses still occurred.

---

## Exact Current Stopping Point

The collector improvements discussed at the end of the previous session have **not yet been implemented**.

The next task is to improve the collector so it behaves as a responsible GitHub API client without reducing the intended product scope.

The agreed direction is:

- Keep authenticated GitHub API requests.
- Keep the intended search-query coverage.
- Process search queries in a controlled sequence.
- Pause between requests.
- Stop the current collector run when GitHub returns a secondary rate-limit response.
- Do not continue sending the remaining queries after GitHub has told the client to back off.
- Print useful failure information.
- Preserve issues successfully collected before the rate limit occurred.

The immediate proposed change is in:

```text
collector/collector/main.py
```

The `httpx.HTTPStatusError` handler should detect:

```text
403
429
```

and stop the current loop.

Conceptual behavior:

```python
except httpx.HTTPStatusError as error:
    failed_queries += 1

    print(f'Search failed: {search_query.name}')
    print(f'GitHub returned HTTP {error.response.status_code}')
    print(f'Response: {error.response.text}')

    if error.response.status_code in (403, 429):
        print()
        print('GitHub rate limit hit. Stopping collector run early.')
        break
```

This has been discussed but not yet added.

Before changing the file, the next session should inspect the current `collector/collector/main.py` exactly as it exists and make the smallest necessary edit.

Do not assume the code matches an earlier example.

---

## Important Product Decision About Collection Scope

A suggestion was made to temporarily reduce the collector to only a few high-signal searches.

The user did not agree with reducing the intended product direction merely because GitHub rate limiting occurred.

The agreed correction is:

- Do not permanently narrow the project to only two search queries.
- Do not treat broad collection as a mistake.
- Improve collector behavior instead.
- Use controlled pacing and safe stopping behavior.
- Continue building toward the actual end product.

The collector should eventually support the intended query coverage responsibly rather than abandoning it.

---

## Phase 2 Direction

Once the collector is stable enough to run responsibly, the next major product capability is rule-based scoring.

The score should estimate whether an issue is worth inspecting based on factors such as:

- Is the issue unassigned?
- Is it recent enough?
- Does it have beginner-friendly labels?
- Does it match preferred task types?
- Is the issue body clear?
- Does it have too many comments?
- Are there signs of disagreement or debate?
- Does the repository appear active?
- Does the task look contained?
- Is the repository archived or disabled?
- Does the issue provide enough information to begin investigating?

The intended classification is:

```text
Look
Maybe
Skip
```

The scoring must be transparent.

The dashboard should eventually explain why an issue received its ranking.

---

## Repository Enrichment Direction

The database schema already contains nullable repository metadata fields:

- Primary language
- Stars
- Forks
- Open issue count
- Archived status
- Disabled status

These fields have not yet been populated.

Repository enrichment will likely require additional GitHub API requests.

Because secondary rate limits are already occurring, enrichment should not be added until collector pacing and rate-limit behavior are handled correctly.

When enrichment begins, avoid repeatedly requesting identical repository metadata for every issue from the same repository.

A suitable design should reuse repository data where practical, but should not introduce unnecessary caching infrastructure or background systems prematurely.

---

## Later AI Direction

AI should only be considered after:

- Collector reliability
- Database storage
- Backend API
- Dashboard
- Repository enrichment
- Rule-based scoring

are working.

Possible later AI-assisted capabilities include:

- Summarizing issue bodies
- Identifying likely task type
- Estimating beginner attemptability
- Detecting red flags
- Explaining why an issue is worth inspecting or skipping
- Comparing issue requirements against the user’s current skill profile
- Producing a short daily report of strong candidates

The AI layer should support the decision process.

It should not present subjective judgments as certainty.

---

## Local Startup Order

### 1. Start PostgreSQL

From the project root:

```powershell
docker compose up -d
```

Purpose:

- Starts the PostgreSQL container in detached mode.

Verify:

```powershell
docker ps
```

Expected container:

```text
github-issue-hunter-postgres
```

### 2. Run the Collector When Needed

From:

```text
collector/
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\activate
```

Run:

```powershell
python -m collector.main
```

The collector should not be run repeatedly in rapid succession while rate-limit handling is still incomplete.

### 3. Start FastAPI

From:

```text
backend/
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\activate
```

Run:

```powershell
fastapi dev app/main.py
```

Expected URL:

```text
http://127.0.0.1:8000
```

Verify:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/health/db
http://127.0.0.1:8000/issues?limit=25
```

### 4. Start Nuxt

From:

```text
frontend/
```

Run:

```powershell
npm run dev
```

Expected URL:

```text
http://localhost:3000/
```

---

## Handoff Instructions for the Next Session

The next session should begin by reviewing this README and then inspecting the actual current collector code.

The first implementation task should be limited to collector rate-limit behavior.

The next session should:

1. Ask for or inspect the current contents of:

   ```text
   collector/collector/main.py
   ```

2. Confirm where the query loop and current exception handlers are located.

3. Make the smallest change necessary to:
   - Preserve the existing delay
   - Stop on rate-limit responses
   - Keep successful results already stored
   - Print a clear message
   - Avoid continuing through the remaining queries after a secondary limit

4. Run the collector once after GitHub’s cooldown period.

5. Confirm the output before moving to repository enrichment or scoring.

Do not immediately rewrite the collector architecture.

Do not introduce:

- Redis
- Celery
- Background workers
- Scheduling infrastructure
- Complex retry frameworks
- New agent frameworks

The immediate task is a small reliability improvement to the working collector.

---

## Current Project Summary

GitHub Issue Hunter has completed its first working end-to-end vertical slice.

The system currently:

- Queries real GitHub issues
- Stores them in PostgreSQL
- Exposes them through FastAPI
- Displays them in a Nuxt dashboard
- Uses a responsive card grid
- Reads a GitHub token from environment configuration
- Has working collector tests
- Has working backend health and issue endpoints

The current blocker is not architecture.

The current issue is that the collector needs responsible rate-limit handling before additional GitHub API-intensive features are added.

The exact next step is:

> Inspect the current collector loop and implement safe stop-on-secondary-rate-limit behavior without reducing the intended product scope.
