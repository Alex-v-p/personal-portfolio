export interface AdminGithubContributionDay {
  date: string;
  count: number;
  level: number;
}

export interface AdminGithubSnapshot {
  id: string;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount?: number | null;
  followingCount?: number | null;
  totalStars?: number | null;
  totalCommits?: number | null;
  rawPayload?: Record<string, unknown> | null;
  contributionDays: AdminGithubContributionDay[];
  createdAt: string;
  updatedAt: string;
}

export interface AdminGithubSnapshotUpsert {
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount?: number | null;
  followingCount?: number | null;
  totalStars?: number | null;
  totalCommits?: number | null;
  rawPayload?: Record<string, unknown> | null;
  contributionDays: AdminGithubContributionDay[];
}

export interface AdminGithubSnapshotRefreshRequest {
  username?: string | null;
  pruneHistory: boolean;
}

export interface AdminAssistantKnowledgeStatus {
  totalDocuments: number;
  totalChunks: number;
  documentsBySourceType: Record<string, number>;
  latestUpdatedAt?: string | null;
}

export interface AdminDashboardSummary {
  projects: number;
  blogPosts: number;
  unreadMessages: number;
  skills: number;
  skillCategories: number;
  mediaFiles: number;
  experiences: number;
  navigationItems: number;
  blogTags: number;
  adminUsers: number;
  githubSnapshots: number;
}
