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
  // server: false,
});
</script>

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
