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
