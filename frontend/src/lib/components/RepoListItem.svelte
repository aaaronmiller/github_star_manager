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

<tr class="border-b border-gray-200 hover:bg-gray-50 transition-colors">
  <td class="py-4 px-6">
    <a href={repo.url} target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 font-medium">
      {repo.name}
    </a>
  </td>
  <td class="py-4 px-6 text-gray-600">
    {repo.description || '—'}
  </td>
  <td class="py-4 px-6 text-center">
    {#if repo.language}
      <span class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
        <span class="inline-block w-2 h-2 rounded-full bg-blue-500"></span>
        {repo.language}
      </span>
    {:else}
      —
    {/if}
  </td>
  <td class="py-4 px-6 text-center">
    {#if repo.stars !== undefined}
      <div class="flex items-center justify-center gap-1">
        <svg class="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        <span>{repo.stars.toLocaleString()}</span>
      </div>
    {:else}
      —
    {/if}
  </td>
  <td class="py-4 px-6 text-center text-gray-600">
    {formattedDate}
  </td>
</tr>
