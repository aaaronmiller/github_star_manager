import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { InstructionsSchema } from '$lib/schemas';
import instructionsData from '$lib/data/instructions.json';
import type { InstructionsMap } from '$lib/types';

export const GET: RequestHandler = async ({ params }) => {
	try {
		const { id } = params;

		const instructions = instructionsData as InstructionsMap;

		if (!instructions[id]) {
			return json(
				{
					error: 'Not Found',
					message: `Instructions for repository '${id}' not found`
				},
				{ status: 404 }
			);
		}

		// Validate the instructions data
		const validatedInstructions = InstructionsSchema.parse(instructions[id]);

		return json(validatedInstructions);
	} catch (error) {
		console.error('Error fetching instructions:', error);
		return json(
			{
				error: 'Internal Server Error',
				message: error instanceof Error ? error.message : 'Unknown error occurred'
			},
			{ status: 500 }
		);
	}
};
