export interface GithubSnapshot {
  id: string;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followerCount: number;
  followingCount: number;
  totalStars: number;
  totalCommits: number;
  rawPayload: Record<string, unknown>;
  createdAt: string;
}
