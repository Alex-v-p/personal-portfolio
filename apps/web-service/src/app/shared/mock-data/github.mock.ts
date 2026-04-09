import { GithubContributionDay } from '../models/github-contribution-day.model';
import { GithubSnapshot } from '../models/github-snapshot.model';

export const GITHUB_SNAPSHOTS: GithubSnapshot[] = [
  {
    id: 'github-snapshot-2025-10-01',
    snapshotDate: '2025-10-01',
    username: 'shuzu',
    publicRepoCount: 24,
    followerCount: 18,
    followingCount: 25,
    totalStars: 37,
    totalCommits: 512,
    rawPayload: { source: 'mock' },
    createdAt: '2025-10-01T08:00:00Z'
  }
];

const contributionLevels = [
  1, 2, 2, 1, 3, 2, 1, 2, 3, 2, 1, 1, 2, 3,
  1, 1, 2, 3, 2, 1, 1, 2, 2, 3, 1, 4, 2, 1,
  1, 2, 1, 2, 3, 1, 2, 2, 4, 2, 1, 2, 3, 1,
  1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2,
  3, 2, 1, 2, 4, 2, 1, 1, 2, 3, 1, 2, 2, 3,
  2, 1, 2, 3, 1, 2, 2, 1, 2, 3, 2, 1, 2, 3
];

export const GITHUB_CONTRIBUTION_DAYS: GithubContributionDay[] = contributionLevels.map((level, index) => ({
  id: `github-day-${index + 1}`,
  snapshotId: GITHUB_SNAPSHOTS[0].id,
  contributionDate: `2025-01-${String((index % 28) + 1).padStart(2, '0')}`,
  contributionCount: level * 3,
  level
}));
