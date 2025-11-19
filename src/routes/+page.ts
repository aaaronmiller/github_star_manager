import type { PageLoad } from './$types';
import type { Repository } from '$lib/types';

export const load: PageLoad = async ({ fetch }) => {
	const response = await fetch('/api/repos');
	const data = await response.json();

	return {
		repositories: data.repositories as Repository[],
		metadata: data.metadata
	};
};
