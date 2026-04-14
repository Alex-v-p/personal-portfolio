export interface GithubContributionDayApi {
  date: string;
  count: number;
  level: number;
}

export interface GithubSnapshotApi {
  id: string;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount?: number | null;
  followingCount?: number | null;
  totalStars?: number | null;
  totalCommits?: number | null;
  createdAt: string;
  contributionDays: GithubContributionDayApi[];
}

export interface StatItemApi {
  id: string;
  label: string;
  value: string;
  description: string;
  actionLabel?: string | null;
  meta?: string | null;
  footnote?: string | null;
}

export interface StatsApi {
  contributionWeeks: number[][];
  githubSummary: StatItemApi;
  latestGithubSnapshot: GithubSnapshotApi;
  portfolioHighlights: StatItemApi[];
  portfolioStats: StatItemApi[];
  monthLabels: string[];
  weekdayLabels: string[];
}
