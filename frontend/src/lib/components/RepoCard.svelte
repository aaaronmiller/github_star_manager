<script lang="ts">
import type { Repository } from '$lib/types';

interface Props {
  repo: Repository;
}

const { repo }: Props = $props();

const formattedDate = $derived(
  repo.lastUpdated
    ? new Date(repo.lastUpdated).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    : 'Unknown',
);
</script>

<article class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
  <a href={repo.url} target="_blank" rel="noopener noreferrer" class="block group">
    <h2 class="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
      {repo.name}
    </h2>
  </a>

  {#if repo.description}
    <p class="text-gray-600 mb-4 line-clamp-2">
      {repo.description}
    </p>
  {/if}

  <div class="flex flex-wrap gap-4 text-sm text-gray-500">
    {#if repo.language}
      <div class="flex items-center gap-1">
        <span class="inline-block w-3 h-3 rounded-full bg-blue-500"></span>
        <span>{repo.language}</span>
      </div>
    {/if}

    {#if repo.stars !== undefined}
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span>{repo.stars.toLocaleString()}</span>
      </div>
    {/if}

    {#if repo.lastUpdated}
      <div class="flex items-center gap-1">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{formattedDate}</span>
      </div>
    {/if}
  </div>
</article>
