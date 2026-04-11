import { GithubSnapshot } from './github-snapshot.model';
import { StatItem } from './stat-item.model';

export interface StatsPageData {
  contributionWeeks: number[][];
  githubSummary: StatItem;
  latestGithubSnapshot: GithubSnapshot | null;
  portfolioHighlights: StatItem[];
  portfolioStats: StatItem[];
  monthLabels: string[];
  weekdayLabels: string[];
}
