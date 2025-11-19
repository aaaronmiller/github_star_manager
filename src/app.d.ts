// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		interface Platform {
			env?: {
				GEMINI_API_KEY?: string;
				GITHUB_TOKEN?: string;
			};
		}
	}
}

export {};
