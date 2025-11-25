import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { RepositorySchema } from '$lib/schemas';
import reposData from '$lib/data/repos.json';
import type { Repository, SortOption } from '$lib/types';
import { z } from 'zod';

export const GET: RequestHandler = async ({ url }) => {
	try {
		const sortParam = url.searchParams.get('sort') as SortOption | null;
		const validSort: SortOption = sortParam && ['dateAdded', 'lastUpdated', 'createdDate'].includes(sortParam)
			? sortParam
			: 'dateAdded';

		// Validate data
		const repos = z.array(RepositorySchema).parse(reposData);

		// Sort repositories
		const sortedRepos = [...repos].sort((a, b) => {
			switch (validSort) {
				case 'lastUpdated':
					return new Date(b.lastUpdatedAt).getTime() - new Date(a.lastUpdatedAt).getTime();
				case 'createdDate':
					return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
				case 'dateAdded':
				default:
					return new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime();
			}
		});

		return json({
			repositories: sortedRepos,
			metadata: {
				totalCount: sortedRepos.length,
				lastScanned: new Date().toISOString()
			}
		});
	} catch (error) {
		console.error('Error fetching repositories:', error);
		return json(
			{
				error: 'Internal Server Error',
				message: error instanceof Error ? error.message : 'Unknown error occurred'
			},
			{ status: 500 }
		);
	}
};
