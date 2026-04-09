import { StatItem } from '../models/stat-item.model';
import { BLOG_POSTS } from './blog-posts.mock';
import { buildContributionWeeks, buildGithubSummary, buildPortfolioStats } from './content.selectors';
import { GITHUB_CONTRIBUTION_DAYS, GITHUB_SNAPSHOTS } from './github.mock';
import { PROJECTS } from './projects.mock';
import { SKILLS } from './skills.mock';

export const LATEST_GITHUB_SNAPSHOT = GITHUB_SNAPSHOTS[0];
export const CONTRIBUTION_WEEKS: number[][] = buildContributionWeeks(GITHUB_CONTRIBUTION_DAYS, LATEST_GITHUB_SNAPSHOT.id);
export const GITHUB_SUMMARY: StatItem = buildGithubSummary(LATEST_GITHUB_SNAPSHOT);

export const PORTFOLIO_HIGHLIGHTS: StatItem[] = [
  {
    id: 'total-views',
    label: 'Total Views',
    value: '500',
    description: 'A placeholder metric for future traffic insights that can later be sourced from site_events.'
  },
  {
    id: 'like-counter',
    label: 'Like Counter',
    value: '500',
    description: 'A placeholder interaction metric for future lightweight engagement on the portfolio.',
    actionLabel: 'Love this portfolio'
  }
];

export const PORTFOLIO_STATS: StatItem[] = buildPortfolioStats(PROJECTS, BLOG_POSTS, SKILLS, LATEST_GITHUB_SNAPSHOT);
