import { GithubSnapshot } from '@domains/stats/model/github-snapshot.model';
import { StatItem } from '@domains/stats/model/stat-item.model';
import { StatsPageData } from '@domains/stats/model/stats-page.model';

import { GithubSnapshotApi, StatItemApi, StatsApi } from './stats.contracts';

export function normalizeGithubSnapshot(snapshot: GithubSnapshotApi): GithubSnapshot {
  return {
    id: snapshot.id,
    snapshotDate: snapshot.snapshotDate,
    username: snapshot.username,
    publicRepoCount: snapshot.publicRepoCount,
    followersCount: snapshot.followersCount ?? 0,
    followingCount: snapshot.followingCount ?? 0,
    totalStars: snapshot.totalStars ?? 0,
    totalCommits: snapshot.totalCommits ?? 0,
    createdAt: snapshot.createdAt,
    contributionDays: (snapshot.contributionDays ?? []).map((day) => ({
      date: day.date,
      count: day.count,
      level: day.level,
    })),
  };
}

export function normalizeStatItem(item: StatItemApi): StatItem {
  return {
    id: item.id,
    label: item.label,
    value: item.value,
    description: item.description,
    actionLabel: item.actionLabel ?? undefined,
    meta: item.meta ?? undefined,
    footnote: item.footnote ?? undefined,
  };
}

export function normalizeStats(stats: StatsApi): StatsPageData {
  return {
    contributionWeeks: stats.contributionWeeks ?? [],
    githubSummary: normalizeStatItem(stats.githubSummary),
    latestGithubSnapshot: normalizeGithubSnapshot(stats.latestGithubSnapshot),
    portfolioHighlights: (stats.portfolioHighlights ?? []).map((item) => normalizeStatItem(item)),
    portfolioStats: (stats.portfolioStats ?? []).map((item) => normalizeStatItem(item)),
    monthLabels: stats.monthLabels ?? [],
    weekdayLabels: stats.weekdayLabels ?? [],
  };
}
