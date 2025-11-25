export interface Repository {
	id: string;
	url: string;
	name: string;
	owner: string;
	summary: string;
	createdAt: string;
	lastUpdatedAt: string;
	addedAt: string;
}

export interface OSInstructions {
	summary: string;
	steps: string[];
	notes?: string;
}

export interface DockerInstructions extends OSInstructions {
	isPreferred: boolean;
	rationale: string;
}

export interface MobileInstructions extends OSInstructions {
	hostOS: string;
	deviceOS: string;
}

export interface Instructions {
	macOS?: OSInstructions;
	windows?: OSInstructions;
	linux?: OSInstructions;
	docker?: DockerInstructions;
	mobile?: MobileInstructions;
}

export type InstructionsMap = Record<string, Instructions>;

export type SortOption = 'dateAdded' | 'lastUpdated' | 'createdDate';
