import { z } from 'zod';

export const OSInstructionsSchema = z.object({
	summary: z.string(),
	steps: z.array(z.string()),
	notes: z.string().optional()
});

export const DockerInstructionsSchema = OSInstructionsSchema.extend({
	isPreferred: z.boolean(),
	rationale: z.string()
});

export const MobileInstructionsSchema = OSInstructionsSchema.extend({
	hostOS: z.string(),
	deviceOS: z.string()
});

export const InstructionsSchema = z.object({
	macOS: OSInstructionsSchema.optional(),
	windows: OSInstructionsSchema.optional(),
	linux: OSInstructionsSchema.optional(),
	docker: DockerInstructionsSchema.optional(),
	mobile: MobileInstructionsSchema.optional()
});

export const RepositorySchema = z.object({
	id: z.string().regex(/^[a-z0-9]+-[a-z0-9_-]+$/),
	url: z.string().url().startsWith('https://github.com/'),
	name: z.string().max(100),
	owner: z.string().max(100),
	summary: z.string().max(500),
	createdAt: z.string().datetime(),
	lastUpdatedAt: z.string().datetime(),
	addedAt: z.string().datetime()
});

export const InstructionsMapSchema = z.record(z.string(), InstructionsSchema);
