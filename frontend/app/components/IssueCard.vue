<script setup lang="ts">
import type { GitHubIssue } from '~/types/issue';

defineProps<{
  issue: GitHubIssue;
}>();

const formatDate = (value: string): string => {
  return new Date(value).toLocaleDateString();
};

const formatLabels = (issue: GitHubIssue): string => {
  return issue.labels
    .map((label) => {
      if (
        typeof label === 'object' &&
        label !== null &&
        'name' in label &&
        typeof label.name === 'string'
      ) {
        return label.name;
      }

      return null;
    })
    .filter((label): label is string => label !== null)
    .join(', ');
};
</script>

<template>
  <article
    class="flex h-full flex-col rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
  >
    <div class="space-y-3">
      <a
        :href="issue.github_issue_url"
        target="_blank"
        rel="noopener noreferrer"
        class="line-clamp-3 text-base font-semibold text-blue-700 hover:underline"
      >
        {{ issue.title }}
      </a>

      <a
        :href="issue.github_repository_url"
        target="_blank"
        rel="noopener noreferrer"
        class="block text-sm font-medium text-gray-600 hover:underline"
      >
        {{ issue.github_repository_full_name }}
      </a>

      <p v-if="issue.body_preview" class="line-clamp-4 text-sm text-gray-700">
        {{ issue.body_preview }}
      </p>

      <div class="flex flex-wrap gap-2 text-xs text-gray-600">
        <span class="rounded bg-gray-100 px-2 py-1">
          Comments: {{ issue.comment_count }}
        </span>

        <span class="rounded bg-gray-100 px-2 py-1">
          Updated: {{ formatDate(issue.github_updated_at) }}
        </span>

        <span class="rounded bg-gray-100 px-2 py-1">
          Assigned: {{ issue.is_assigned ? 'Yes' : 'No' }}
        </span>
      </div>

      <div class="text-xs text-gray-500">
        <span class="font-medium">Labels:</span>
        {{ formatLabels(issue) || 'None' }}
      </div>

      <div class="text-xs text-gray-500">
        <span class="font-medium">Source:</span>
        {{ issue.source_query }}
      </div>
    </div>
  </article>
</template>
