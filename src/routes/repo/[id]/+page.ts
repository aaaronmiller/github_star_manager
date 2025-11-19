import type { PageLoad } from './$types';
import type { Repository, Instructions } from '$lib/types';

export const load: PageLoad = async ({ params, fetch }) => {
	const { id } = params;

	// Fetch repository details
	const reposResponse = await fetch('/api/repos');
	const reposData = await reposResponse.json();
	const repository = reposData.repositories.find((r: Repository) => r.id === id);

	if (!repository) {
		throw new Error(`Repository ${id} not found`);
	}

	// Fetch installation instructions
	const instructionsResponse = await fetch(`/api/instructions/${id}`);
	const instructions: Instructions = await instructionsResponse.json();

	return {
		repository,
		instructions
	};
};
