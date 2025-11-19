import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { z } from 'zod';

const AddRepoRequestSchema = z.object({
	urls: z.array(z.string().url())
});

export const POST: RequestHandler = async ({ request, platform }) => {
	try {
		const body = await request.json();
		const { urls } = AddRepoRequestSchema.parse(body);

		// Validate GitHub URLs
		const githubUrls = urls.filter(url => url.startsWith('https://github.com/'));

		if (githubUrls.length === 0) {
			return json(
				{
					error: 'Bad Request',
					message: 'No valid GitHub repository URLs provided'
				},
				{ status: 400 }
			);
		}

		// Get Gemini API key from environment
		const geminiApiKey = platform?.env?.GEMINI_API_KEY;

		if (!geminiApiKey) {
			return json(
				{
					error: 'Configuration Error',
					message: 'GEMINI_API_KEY not configured. Please set up the environment variable.'
				},
				{ status: 500 }
			);
		}

		const results = [];

		for (const url of githubUrls) {
			try {
				// Extract owner and repo name from URL
				const match = url.match(/github\.com\/([^\/]+)\/([^\/]+)/);
				if (!match) {
					results.push({
						url,
						success: false,
						error: 'Invalid GitHub URL format'
					});
					continue;
				}

				const [, owner, repoName] = match;
				const id = `${owner.toLowerCase()}-${repoName.toLowerCase().replace(/\./g, '_')}`;

				// Construct the Gemini prompt
				const prompt = `You are an expert software engineering analyst. Your task is to analyze a GitHub repository and extract key metadata and installation instructions. You MUST return your response as a single, valid JSON object and nothing else.

The repository URL is: ${url}

Required JSON output format:
{
  "id": "${id}",
  "url": "${url}",
  "name": "${repoName}",
  "owner": "${owner}",
  "summary": "A concise, one-paragraph summary of what this repository is for and its key features.",
  "createdAt": "ISO 8601 format",
  "lastUpdatedAt": "ISO 8601 format",
  "instructions": {
    "macOS": { "summary": "...", "steps": ["...", "..."], "notes": "..." },
    "windows": { "summary": "...", "steps": ["...", "..."], "notes": "..." },
    "linux": { "summary": "...", "steps": ["...", "..."], "notes": "..." },
    "docker": {
      "summary": "...",
      "steps": ["...", "..."],
      "notes": "...",
      "isPreferred": boolean,
      "rationale": "..."
    }
  }
}

Instructions:
1. Use exact 'id', 'url', 'name', 'owner' values provided above.
2. Fetch the repository page and create comprehensive yet brief summary from the README.
3. For timestamps, use current time in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
4. For each OS: provide installation summary, exact shell commands in 'steps', prerequisites in 'notes'.
5. If no instructions found for specific OS, return empty object {}.
6. Set 'docker.isPreferred' to true only if documentation explicitly recommends Docker.
7. Provide clear rationale for Docker preference decision.
8. Return ONLY the JSON object, no markdown formatting or additional text.`;

				// Call Gemini API
				const geminiResponse = await fetch(
					`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${geminiApiKey}`,
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify({
							contents: [{
								parts: [{
									text: prompt
								}]
							}],
							generationConfig: {
								temperature: 0.2,
								topK: 40,
								topP: 0.95,
								maxOutputTokens: 2048,
							}
						})
					}
				);

				if (!geminiResponse.ok) {
					const errorText = await geminiResponse.text();
					results.push({
						url,
						success: false,
						error: `Gemini API error: ${geminiResponse.status} - ${errorText}`
					});
					continue;
				}

				const geminiData = await geminiResponse.json();
				const generatedText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text;

				if (!generatedText) {
					results.push({
						url,
						success: false,
						error: 'No response from Gemini API'
					});
					continue;
				}

				// Extract JSON from response (in case it's wrapped in markdown)
				let extractedJson = generatedText.trim();
				if (extractedJson.startsWith('```json')) {
					extractedJson = extractedJson.replace(/```json\n?/, '').replace(/\n?```$/, '').trim();
				} else if (extractedJson.startsWith('```')) {
					extractedJson = extractedJson.replace(/```\n?/, '').replace(/\n?```$/, '').trim();
				}

				const parsedData = JSON.parse(extractedJson);

				results.push({
					url,
					success: true,
					data: parsedData
				});

			} catch (error) {
				results.push({
					url,
					success: false,
					error: error instanceof Error ? error.message : 'Unknown error'
				});
			}
		}

		return json({
			success: true,
			results,
			message: `Processed ${results.length} repository URL(s). Manual commit required to persist data.`
		});

	} catch (error) {
		console.error('Error in add-repo endpoint:', error);
		return json(
			{
				error: 'Internal Server Error',
				message: error instanceof Error ? error.message : 'Unknown error occurred'
			},
			{ status: 500 }
		);
	}
};
