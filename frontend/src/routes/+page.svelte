<script lang="ts">
import RepoCard from '$lib/components/RepoCard.svelte';
import RepoListItem from '$lib/components/RepoListItem.svelte';
import type { ReposData } from '$lib/types';

let data = $state<ReposData | null>(null);
let loading = $state(true);
let error = $state<string | null>(null);
let viewMode = $state<'grid' | 'list'>('grid');

async function loadRepos() {
  try {
    loading = true;
    error = null;

    const response = await fetch('/api/repos');

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Failed to fetch repositories');
    }

    data = await response.json();
  } catch (e) {
    error = e instanceof Error ? e.message : 'An unexpected error occurred';
    console.error('Failed to load repositories:', e);
  } finally {
    loading = false;
  }
}

$effect(() => {
  loadRepos();
});

const formattedLastScanned = $derived(
  data?.metadata?.lastScanned
    ? new Date(data.metadata.lastScanned).toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : 'Unknown',
);
</script>

<svelte:head>
  <title>GitHub Star Manager</title>
  <meta name="description" content="Manage and visualize your GitHub starred repositories" />
</svelte:head>

<main class="container mx-auto px-4 py-8 max-w-7xl">
  <header class="mb-8">
    <h1 class="text-4xl font-bold text-gray-900 mb-2">
      GitHub Star Manager
    </h1>
    <p class="text-gray-600">
      Manage and visualize your GitHub starred repositories
    </p>
  </header>

  {#if loading}
    <div class="flex items-center justify-center py-20">
      <div class="text-center">
        <div class="inline-block w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
        <p class="text-gray-600">Loading repositories...</p>
      </div>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
      <div class="flex items-start gap-3">
        <svg class="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h2 class="text-lg font-semibold text-red-900 mb-1">Error Loading Repositories</h2>
          <p class="text-red-700">{error}</p>
          <button
            onclick={loadRepos}
            class="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  {:else if data}
    <div class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div class="text-gray-600">
        <p class="font-medium">
          {data.metadata.totalCount} {data.metadata.totalCount === 1 ? 'repository' : 'repositories'}
        </p>
        <p class="text-sm">Last scanned: {formattedLastScanned}</p>
      </div>

      <div class="flex items-center gap-2 bg-white rounded-lg shadow-sm p-1">
        <button
          onclick={() => viewMode = 'grid'}
          class="flex items-center gap-2 px-4 py-2 rounded-md transition-colors {viewMode === 'grid' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}"
          aria-label="Grid view"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
          <span class="hidden sm:inline">Grid</span>
        </button>
        <button
          onclick={() => viewMode = 'list'}
          class="flex items-center gap-2 px-4 py-2 rounded-md transition-colors {viewMode === 'list' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-100'}"
          aria-label="List view"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <span class="hidden sm:inline">List</span>
        </button>
      </div>
    </div>

    {#if data.repositories.length === 0}
      <div class="bg-gray-100 rounded-lg p-12 text-center">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
        </svg>
        <h2 class="text-xl font-semibold text-gray-700 mb-2">No Repositories Found</h2>
        <p class="text-gray-600">Run the CLI tool to scan and import your repositories.</p>
      </div>
    {:else if viewMode === 'grid'}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each data.repositories as repo (repo.url)}
          <RepoCard {repo} />
        {/each}
      </div>
    {:else}
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-100 border-b border-gray-200">
              <tr>
                <th class="py-3 px-6 text-left text-sm font-semibold text-gray-700">Name</th>
                <th class="py-3 px-6 text-left text-sm font-semibold text-gray-700">Description</th>
                <th class="py-3 px-6 text-center text-sm font-semibold text-gray-700">Language</th>
                <th class="py-3 px-6 text-center text-sm font-semibold text-gray-700">Stars</th>
                <th class="py-3 px-6 text-center text-sm font-semibold text-gray-700">Last Updated</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repositories as repo (repo.url)}
                <RepoListItem {repo} />
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    {/if}
  {/if}
</main>
