export interface AdminGithubContributionDay {
  date: string;
  count: number;
  level: number;
}

export type AdminGithubAutoRefreshStatus = 'scheduled' | 'retry_scheduled' | 'due' | 'disabled' | 'manual_only';

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
  autoRefreshEnabled: boolean;
  autoRefreshStatus: AdminGithubAutoRefreshStatus;
  nextAutoRefreshAt?: string | null;
  secondsUntilAutoRefresh?: number | null;
}

export interface AdminGithubSnapshotsResponse {
  items: AdminGithubSnapshot[];
  total: number;
  autoRefreshEnabled: boolean;
  autoRefreshUsername?: string | null;
  autoRefreshIntervalSeconds?: number | null;
  autoRefreshRetryIntervalSeconds?: number | null;
  autoRefreshStatus: AdminGithubAutoRefreshStatus;
  nextAutoRefreshAt?: string | null;
  secondsUntilAutoRefresh?: number | null;
  lastAutoRefreshAt?: string | null;
  lastAutoRefreshFailedAt?: string | null;
  autoRefreshError?: string | null;
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
