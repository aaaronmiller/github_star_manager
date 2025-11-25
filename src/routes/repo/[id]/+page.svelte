<script lang="ts">
	import type { PageData } from './$types';
	import type { OSInstructions, DockerInstructions, MobileInstructions } from '$lib/types';

	let { data }: { data: PageData } = $props();

	type OSKey = 'macOS' | 'windows' | 'linux' | 'docker' | 'mobile';

	let activeTab = $state<OSKey>('macOS');

	const availableTabs = $derived(() => {
		const tabs: OSKey[] = [];
		if (data.instructions.macOS && Object.keys(data.instructions.macOS).length > 0) tabs.push('macOS');
		if (data.instructions.windows && Object.keys(data.instructions.windows).length > 0) tabs.push('windows');
		if (data.instructions.linux && Object.keys(data.instructions.linux).length > 0) tabs.push('linux');
		if (data.instructions.docker && Object.keys(data.instructions.docker).length > 0) tabs.push('docker');
		if (data.instructions.mobile && Object.keys(data.instructions.mobile).length > 0) tabs.push('mobile');
		return tabs;
	});

	$effect(() => {
		if (availableTabs().length > 0 && !availableTabs().includes(activeTab)) {
			activeTab = availableTabs()[0];
		}
	});

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}

	function copyToClipboard(text: string) {
		navigator.clipboard.writeText(text);
	}

	function isDockerInstructions(instructions: OSInstructions | DockerInstructions | MobileInstructions | undefined): instructions is DockerInstructions {
		return instructions !== undefined && 'isPreferred' in instructions;
	}

	function isMobileInstructions(instructions: OSInstructions | DockerInstructions | MobileInstructions | undefined): instructions is MobileInstructions {
		return instructions !== undefined && 'hostOS' in instructions;
	}
</script>

<div>
	<div class="mb-6">
		<a href="/" class="text-blue-600 hover:text-blue-700 text-sm font-medium">
			← Back to Dashboard
		</a>
	</div>

	<!-- Repository Header -->
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
		<div class="flex items-start justify-between mb-4">
			<div>
				<h1 class="text-3xl font-bold text-gray-900 mb-2">
					{data.repository.owner}/{data.repository.name}
				</h1>
				<a
					href={data.repository.url}
					target="_blank"
					rel="noopener noreferrer"
					class="text-blue-600 hover:text-blue-700 text-sm"
				>
					View on GitHub →
				</a>
			</div>
		</div>

		<p class="text-gray-700 mb-6 leading-relaxed">
			{data.repository.summary}
		</p>

		<div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
			<div>
				<span class="text-sm font-medium text-gray-500">Created</span>
				<p class="text-gray-900">{formatDate(data.repository.createdAt)}</p>
			</div>
			<div>
				<span class="text-sm font-medium text-gray-500">Last Updated</span>
				<p class="text-gray-900">{formatDate(data.repository.lastUpdatedAt)}</p>
			</div>
			<div>
				<span class="text-sm font-medium text-gray-500">Added to Dashboard</span>
				<p class="text-gray-900">{formatDate(data.repository.addedAt)}</p>
			</div>
		</div>
	</div>

	<!-- Installation Instructions -->
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
		<div class="border-b border-gray-200 px-6 py-4">
			<h2 class="text-xl font-semibold text-gray-900">Installation Instructions</h2>
		</div>

		<!-- Tabs -->
		{#if availableTabs().length > 0}
			<div class="border-b border-gray-200 px-6">
				<nav class="flex gap-6 -mb-px">
					{#each availableTabs() as tab}
						<button
							onclick={() => (activeTab = tab)}
							class="py-4 px-1 border-b-2 font-medium text-sm transition-colors"
							class:border-blue-600={activeTab === tab}
							class:text-blue-600={activeTab === tab}
							class:border-transparent={activeTab !== tab}
							class:text-gray-500={activeTab !== tab}
							class:hover:text-gray-700={activeTab !== tab}
						>
							{tab === 'macOS' ? 'macOS' : tab.charAt(0).toUpperCase() + tab.slice(1)}
						</button>
					{/each}
				</nav>
			</div>

			<!-- Tab Content -->
			<div class="p-6">
				{#if activeTab === 'macOS' && data.instructions.macOS}
					{@const instructions = data.instructions.macOS}
					<div class="mb-4">
						<h3 class="text-lg font-semibold text-gray-900 mb-2">Summary</h3>
						<p class="text-gray-700">{instructions.summary}</p>
					</div>

					{#if instructions.steps && instructions.steps.length > 0}
						<div class="mb-4">
							<h3 class="text-lg font-semibold text-gray-900 mb-3">Installation Steps</h3>
							<ol class="space-y-3">
								{#each instructions.steps as step, index}
									<li class="flex gap-3">
										<span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
											{index + 1}
										</span>
										<div class="flex-1">
											<code class="text-sm bg-gray-50 px-2 py-1 rounded block overflow-x-auto">
												{step}
											</code>
											<button
												onclick={() => copyToClipboard(step)}
												class="text-xs text-blue-600 hover:text-blue-700 mt-1"
											>
												Copy
											</button>
										</div>
									</li>
								{/each}
							</ol>
						</div>
					{/if}

					{#if instructions.notes}
						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-yellow-900 mb-1">Notes</h4>
							<p class="text-sm text-yellow-800">{instructions.notes}</p>
						</div>
					{/if}
				{:else if activeTab === 'windows' && data.instructions.windows}
					{@const instructions = data.instructions.windows}
					<div class="mb-4">
						<h3 class="text-lg font-semibold text-gray-900 mb-2">Summary</h3>
						<p class="text-gray-700">{instructions.summary}</p>
					</div>

					{#if instructions.steps && instructions.steps.length > 0}
						<div class="mb-4">
							<h3 class="text-lg font-semibold text-gray-900 mb-3">Installation Steps</h3>
							<ol class="space-y-3">
								{#each instructions.steps as step, index}
									<li class="flex gap-3">
										<span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
											{index + 1}
										</span>
										<div class="flex-1">
											<code class="text-sm bg-gray-50 px-2 py-1 rounded block overflow-x-auto">
												{step}
											</code>
											<button
												onclick={() => copyToClipboard(step)}
												class="text-xs text-blue-600 hover:text-blue-700 mt-1"
											>
												Copy
											</button>
										</div>
									</li>
								{/each}
							</ol>
						</div>
					{/if}

					{#if instructions.notes}
						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-yellow-900 mb-1">Notes</h4>
							<p class="text-sm text-yellow-800">{instructions.notes}</p>
						</div>
					{/if}
				{:else if activeTab === 'linux' && data.instructions.linux}
					{@const instructions = data.instructions.linux}
					<div class="mb-4">
						<h3 class="text-lg font-semibold text-gray-900 mb-2">Summary</h3>
						<p class="text-gray-700">{instructions.summary}</p>
					</div>

					{#if instructions.steps && instructions.steps.length > 0}
						<div class="mb-4">
							<h3 class="text-lg font-semibold text-gray-900 mb-3">Installation Steps</h3>
							<ol class="space-y-3">
								{#each instructions.steps as step, index}
									<li class="flex gap-3">
										<span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
											{index + 1}
										</span>
										<div class="flex-1">
											<code class="text-sm bg-gray-50 px-2 py-1 rounded block overflow-x-auto">
												{step}
											</code>
											<button
												onclick={() => copyToClipboard(step)}
												class="text-xs text-blue-600 hover:text-blue-700 mt-1"
											>
												Copy
											</button>
										</div>
									</li>
								{/each}
							</ol>
						</div>
					{/if}

					{#if instructions.notes}
						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-yellow-900 mb-1">Notes</h4>
							<p class="text-sm text-yellow-800">{instructions.notes}</p>
						</div>
					{/if}
				{:else if activeTab === 'docker' && data.instructions.docker}
					{@const instructions = data.instructions.docker}
					{#if isDockerInstructions(instructions)}
						{#if instructions.isPreferred}
							<div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
								<h4 class="text-sm font-semibold text-green-900 mb-1">✓ Recommended Approach</h4>
								<p class="text-sm text-green-800">{instructions.rationale}</p>
							</div>
						{:else}
							<div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
								<h4 class="text-sm font-semibold text-blue-900 mb-1">Docker Available</h4>
								<p class="text-sm text-blue-800">{instructions.rationale}</p>
							</div>
						{/if}
					{/if}

					<div class="mb-4">
						<h3 class="text-lg font-semibold text-gray-900 mb-2">Summary</h3>
						<p class="text-gray-700">{instructions.summary}</p>
					</div>

					{#if instructions.steps && instructions.steps.length > 0}
						<div class="mb-4">
							<h3 class="text-lg font-semibold text-gray-900 mb-3">Installation Steps</h3>
							<ol class="space-y-3">
								{#each instructions.steps as step, index}
									<li class="flex gap-3">
										<span class="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
											{index + 1}
										</span>
										<div class="flex-1">
											<code class="text-sm bg-gray-50 px-2 py-1 rounded block overflow-x-auto">
												{step}
											</code>
											<button
												onclick={() => copyToClipboard(step)}
												class="text-xs text-blue-600 hover:text-blue-700 mt-1"
											>
												Copy
											</button>
										</div>
									</li>
								{/each}
							</ol>
						</div>
					{/if}

					{#if instructions.notes}
						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-yellow-900 mb-1">Notes</h4>
							<p class="text-sm text-yellow-800">{instructions.notes}</p>
						</div>
					{/if}
				{:else if activeTab === 'mobile' && data.instructions.mobile}
					{@const instructions = data.instructions.mobile}
					{#if isMobileInstructions(instructions)}
						<div class="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
							<h4 class="text-sm font-semibold text-purple-900 mb-1">Host-Device Setup</h4>
							<p class="text-sm text-purple-800">
								Host OS: {instructions.hostOS} | Device OS: {instructions.deviceOS}
							</p>
						</div>
					{/if}

					<div class="mb-4">
						<h3 class="text-lg font-semibold text-gray-900 mb-2">Summary</h3>
						<p class="text-gray-700">{instructions.summary}</p>
					</div>

					{#if instructions.steps && instructions.steps.length > 0}
						<div class="mb-4">
							<h3 class="text-lg font-semibold text-gray-900 mb-3">Installation Steps</h3>
							<ol class="space-y-3">
								{#each instructions.steps as step, index}
									<li class="flex gap-3">
										<span class="flex-shrink-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
											{index + 1}
										</span>
										<div class="flex-1">
											<code class="text-sm bg-gray-50 px-2 py-1 rounded block overflow-x-auto">
												{step}
											</code>
											<button
												onclick={() => copyToClipboard(step)}
												class="text-xs text-blue-600 hover:text-blue-700 mt-1"
											>
												Copy
											</button>
										</div>
									</li>
								{/each}
							</ol>
						</div>
					{/if}

					{#if instructions.notes}
						<div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
							<h4 class="text-sm font-semibold text-yellow-900 mb-1">Notes</h4>
							<p class="text-sm text-yellow-800">{instructions.notes}</p>
						</div>
					{/if}
				{/if}
			</div>
		{:else}
			<div class="p-8 text-center">
				<p class="text-gray-500">No installation instructions available for this repository.</p>
				<a
					href={data.repository.url}
					target="_blank"
					rel="noopener noreferrer"
					class="text-blue-600 hover:text-blue-700 text-sm mt-2 inline-block"
				>
					View README on GitHub →
				</a>
			</div>
		{/if}
	</div>
</div>
