export interface Repository {
  name: string;
  url: string;
  description?: string;
  stars?: number;
  language?: string;
  lastUpdated?: string;
}

export interface Metadata {
  totalCount: number;
  lastScanned: string;
}

export interface ReposData {
  repositories: Repository[];
  metadata: Metadata;
}
