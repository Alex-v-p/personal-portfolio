import { GithubContributionDay } from './github-contribution-day.model';

export interface GithubSnapshot {
  id: string;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount: number;
  followingCount: number;
  totalStars: number;
  totalCommits: number;
  createdAt: string;
  contributionDays: GithubContributionDay[];
}
