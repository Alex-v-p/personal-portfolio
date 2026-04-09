import { StatItem } from '../models/stat-item.model';
import { BLOG_POSTS } from './blog-posts.mock';
import { buildContributionCells, buildGithubSummary, buildPortfolioStats } from './content.selectors';
import { GITHUB_CONTRIBUTION_DAYS, GITHUB_SNAPSHOTS } from './github.mock';
import { PROJECTS } from './projects.mock';
import { SKILLS } from './skills.mock';

export const LATEST_GITHUB_SNAPSHOT = GITHUB_SNAPSHOTS[0];
export const CONTRIBUTION_CELLS: number[] = buildContributionCells(GITHUB_CONTRIBUTION_DAYS, LATEST_GITHUB_SNAPSHOT.id);
export const GITHUB_SUMMARY: StatItem = buildGithubSummary(LATEST_GITHUB_SNAPSHOT);
export const PORTFOLIO_STATS: StatItem[] = buildPortfolioStats(PROJECTS, BLOG_POSTS, SKILLS, LATEST_GITHUB_SNAPSHOT);
