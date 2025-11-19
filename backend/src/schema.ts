import { z } from 'zod';

export const RepositorySchema = z.object({
  name: z.string().min(1, 'Repository name is required'),
  url: z.string().url('Must be a valid URL'),
  description: z.string().optional(),
  stars: z.number().int().nonnegative().optional(),
  language: z.string().optional(),
  lastUpdated: z.string().datetime().optional(),
});

export const MetadataSchema = z.object({
  totalCount: z.number().int().nonnegative(),
  lastScanned: z.string().datetime(),
});

export const ReposDataSchema = z.object({
  repositories: z.array(RepositorySchema),
  metadata: MetadataSchema,
});

export type Repository = z.infer<typeof RepositorySchema>;
export type Metadata = z.infer<typeof MetadataSchema>;
export type ReposData = z.infer<typeof ReposDataSchema>;
