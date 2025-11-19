<script lang="ts">
	import type { PageData } from './$types';
	import type { SortOption } from '$lib/types';

	let { data }: { data: PageData } = $props();

	let searchQuery = $state('');
	let sortBy = $state<SortOption>('dateAdded');
	let addRepoUrl = $state('');
	let isAdding = $state(false);
	let addMessage = $state('');

	const sortedAndFilteredRepos = $derived(() => {
		let repos = [...data.repositories];

		// Filter by search query
		if (searchQuery) {
			const query = searchQuery.toLowerCase();
			repos = repos.filter(
				(repo) =>
					repo.name.toLowerCase().includes(query) ||
					repo.owner.toLowerCase().includes(query) ||
					repo.summary.toLowerCase().includes(query)
			);
		}

		// Sort
		repos.sort((a, b) => {
			switch (sortBy) {
				case 'lastUpdated':
					return new Date(b.lastUpdatedAt).getTime() - new Date(a.lastUpdatedAt).getTime();
				case 'createdDate':
					return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
				case 'dateAdded':
				default:
					return new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime();
			}
		});

		return repos;
	});

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	async function handleAddRepo() {
		if (!addRepoUrl.trim()) return;

		isAdding = true;
		addMessage = '';

		try {
			const response = await fetch('/api/add-repo', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					urls: [addRepoUrl.trim()]
				})
			});

			const result = await response.json();

			if (response.ok) {
				addMessage = 'Repository analyzed successfully! Data ready for commit.';
				addRepoUrl = '';
			} else {
				addMessage = `Error: ${result.message || 'Failed to add repository'}`;
			}
		} catch (error) {
			addMessage = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
		} finally {
			isAdding = false;
		}
	}
</script>

<div>
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900 mb-2">Repository Dashboard</h1>
		<p class="text-gray-600">
			Manage and explore your curated GitHub repositories with AI-powered insights
		</p>
	</div>

	<!-- Add Repository Section -->
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
		<h2 class="text-lg font-semibold text-gray-900 mb-4">Add New Repository</h2>
		<div class="flex gap-3">
			<input
				type="url"
				bind:value={addRepoUrl}
				placeholder="https://github.com/owner/repo"
				class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
				disabled={isAdding}
			/>
			<button
				onclick={handleAddRepo}
				disabled={isAdding || !addRepoUrl.trim()}
				class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed font-medium"
			>
				{isAdding ? 'Analyzing...' : 'Add Repository'}
			</button>
		</div>
		{#if addMessage}
			<p class="mt-3 text-sm" class:text-green-600={!addMessage.startsWith('Error')} class:text-red-600={addMessage.startsWith('Error')}>
				{addMessage}
			</p>
		{/if}
	</div>

	<!-- Controls -->
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
		<div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
			<div class="flex-1 w-full sm:w-auto">
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search repositories..."
					class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
				/>
			</div>

			<div class="flex items-center gap-2">
				<label for="sort" class="text-sm font-medium text-gray-700 whitespace-nowrap">
					Sort by:
				</label>
				<select
					id="sort"
					bind:value={sortBy}
					class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
				>
					<option value="dateAdded">Date Added</option>
					<option value="lastUpdated">Last Updated</option>
					<option value="createdDate">Created Date</option>
				</select>
			</div>
		</div>

		{#if searchQuery}
			<div class="mt-3 flex items-center gap-2">
				<span class="text-sm text-gray-600">
					{sortedAndFilteredRepos().length} result(s) found
				</span>
				<button
					onclick={() => (searchQuery = '')}
					class="text-sm text-blue-600 hover:text-blue-700"
				>
					Clear filter
				</button>
			</div>
		{/if}
	</div>

	<!-- Repository Grid -->
	<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
		{#each sortedAndFilteredRepos() as repo (repo.id)}
			<a
				href="/repo/{repo.id}"
				class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
			>
				<div class="flex items-start justify-between mb-3">
					<h3 class="text-lg font-semibold text-gray-900 break-words">
						{repo.owner}/{repo.name}
					</h3>
				</div>

				<p class="text-sm text-gray-600 mb-4 line-clamp-3">
					{repo.summary}
				</p>

				<div class="space-y-1 text-xs text-gray-500">
					<div class="flex items-center gap-2">
						<span class="font-medium">Created:</span>
						<span>{formatDate(repo.createdAt)}</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="font-medium">Updated:</span>
						<span>{formatDate(repo.lastUpdatedAt)}</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="font-medium">Added:</span>
						<span>{formatDate(repo.addedAt)}</span>
					</div>
				</div>

				<div class="mt-4 pt-4 border-t border-gray-200">
					<span class="text-sm text-blue-600 hover:text-blue-700 font-medium">
						View Installation →
					</span>
				</div>
			</a>
		{:else}
			<div class="col-span-full text-center py-12">
				<p class="text-gray-500">No repositories found.</p>
			</div>
		{/each}
	</div>

	{#if !searchQuery}
		<div class="mt-8 text-center text-sm text-gray-500">
			Showing {data.repositories.length} total repositories
		</div>
	{/if}
</div>
