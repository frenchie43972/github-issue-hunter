-- GitHub Issue Hunter
-- Phase 1 database schema
--
-- Purpose:
--   Creates the initial issues table used by the Python collector,
--   FastAPI backend, and Nuxt dashboard.
--
-- Notes:
-- GitHub Issue Hunter
-- Initial GitHub issues table
--
-- Purpose:
--   Stores issues collected by the GitHub Issue Collector Agent.
--
-- Design intent:
--   This table is not a throwaway prototype table. It is the first durable
--   storage model for GitHub issue data in a system that may later include
--   scoring, AI review, reporting, and additional collection agents.
--
-- Scope:
--   This table stores the canonical GitHub issue record as collected from
--   GitHub. Future derived outputs, such as rule-based scores or AI review
--   results, should usually live in separate tables so this source record
--   remains clean.

CREATE TABLE IF NOT EXISTS github_issues (
    -- GENERATED ALWAYS means normal application code should not provide
    -- this value manually. PostgreSQL owns it.
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    github_issue_id BIGINT NOT NULL UNIQUE,
    -- GitHub's global node ID.
    github_node_id TEXT,
    github_issue_number INTEGER NOT NULL,
    github_repository_owner TEXT NOT NULL,
    github_repository_name TEXT NOT NULL,
    github_repository_full_name TEXT NOT NULL,
    github_repository_id BIGINT,
    github_issue_url TEXT NOT NULL,
    github_repository_url TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    body_preview TEXT,

    -- GitHub issue state at collection time.
    --
    -- Expected values are usually 'open' or 'closed'. The collector will
    -- initially search open issues, but storing state keeps the record
    -- accurate if an issue later closes.
    state TEXT NOT NULL,

    -- GitHub labels attached to the issue.
    --
    -- Stored as JSONB because GitHub labels are naturally structured data
    -- and we do not need a separate labels table yet.
    --
    -- Example:
    --   [
    --     {"name": "documentation", "color": "0075ca"},
    --     {"name": "good first issue", "color": "7057ff"}
    --   ]
    labels JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- True when the issue has one or more assignees.
    --
    -- The collector will usually search for unassigned issues, but this is
    -- still stored because assignment status can change over time.
    is_assigned BOOLEAN NOT NULL DEFAULT FALSE,
    assignee_count INTEGER NOT NULL DEFAULT 0,
    comment_count INTEGER NOT NULL DEFAULT 0,
    repository_primary_language TEXT,
    repository_stars INTEGER,
    repository_forks INTEGER,
    repository_open_issues_count INTEGER,
    repository_is_archived BOOLEAN,
    repository_is_disabled BOOLEAN,

    -- The GitHub search query that found this issue.
    --
    -- This is important audit/debug metadata for understanding why the
    -- collector stored a given issue.
    source_query TEXT NOT NULL,

    -- Name of the collector that produced this record.
    --
    -- Keeping this now makes the database ready for multiple future
    -- collectors without redesigning the base table.
    collected_by TEXT NOT NULL DEFAULT 'github_issue_collector',
    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    github_created_at TIMESTAMPTZ NOT NULL,
    github_updated_at TIMESTAMPTZ NOT NULL,
    github_closed_at TIMESTAMPTZ,

    -- Enforces one local row per issue
    CONSTRAINT uq_github_issues_github_issue_id
        UNIQUE (github_issue_id),

    -- Enforces one local row per public GitHub issue URL.
    --
    -- This is somewhat redundant with github_issue_id, but useful as a
    -- second guard because issue URLs are central to the dashboard.
    CONSTRAINT uq_github_issues_github_issue_url
        UNIQUE (github_issue_url),

    -- Prevents invalid negative counts.
    CONSTRAINT chk_github_issues_assignee_count_nonnegative
        CHECK (assignee_count >= 0),

    -- Prevents invalid negative comment counts.
    CONSTRAINT chk_github_issues_comment_count_nonnegative
        CHECK (comment_count >= 0),

    -- Prevents invalid negative repository star counts when present.
    CONSTRAINT chk_github_issues_repository_stars_nonnegative
        CHECK (repository_stars IS NULL OR repository_stars >= 0),

    -- Prevents invalid negative repository fork counts when present.
    CONSTRAINT chk_github_issues_repository_forks_nonnegative
        CHECK (repository_forks IS NULL OR repository_forks >= 0),

    -- Keeps the state field constrained to known GitHub issue states.
    CONSTRAINT chk_github_issues_state
        CHECK (state IN ('open', 'closed'))
);

    -- Supports dashboard sorting by newest collected records.
    CREATE INDEX IF NOT EXISTS idx_github_issues_collected_at
    ON github_issues (collected_at DESC);

    -- Supports dashboard sorting by recently updated GitHub issues.
    CREATE INDEX IF NOT EXISTS idx_github_issues_github_updated_at
    ON github_issues (github_updated_at DESC);

    -- Supports filtering by repository.
    CREATE INDEX IF NOT EXISTS idx_github_issues_repository_full_name
    ON github_issues (github_repository_full_name);

    -- Supports filtering by source query.
    CREATE INDEX IF NOT EXISTS idx_github_issues_source_query
    ON github_issues (source_query);

    -- Supports filtering for unassigned or assigned issues.
    CREATE INDEX IF NOT EXISTS idx_github_issues_is_assigned
    ON github_issues (is_assigned);

    -- Supports filtering by repository language.
    CREATE INDEX IF NOT EXISTS idx_github_issues_repository_primary_language
    ON github_issues (repository_primary_language);

    -- Supports filtering by open or closed state.
    CREATE INDEX IF NOT EXISTS idx_github_issues_state
    ON github_issues (state);

    -- Supports future queries that inspect label JSON content.
    --
    -- This is useful if later filtering needs to ask questions like:
    --   Does labels contain a label named "good first issue"?
    CREATE INDEX IF NOT EXISTS idx_github_issues_labels_gin
    ON github_issues USING GIN (labels);