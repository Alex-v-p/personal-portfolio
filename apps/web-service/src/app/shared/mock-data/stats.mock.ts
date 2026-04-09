import { BLOG_POSTS } from './blog-posts.mock';
import { PROJECTS } from './projects.mock';
import { StatItem } from '../models/stat-item.model';

export const CONTRIBUTION_CELLS: number[] = [
  1, 2, 2, 1, 3, 2, 1, 2, 3, 2, 1, 1, 2, 3,
  1, 1, 2, 3, 2, 1, 1, 2, 2, 3, 1, 4, 2, 1,
  1, 2, 1, 2, 3, 1, 2, 2, 4, 2, 1, 2, 3, 1,
  1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 2,
  3, 2, 1, 2, 4, 2, 1, 1, 2, 3, 1, 2, 2, 3,
  2, 1, 2, 3, 1, 2, 2, 1, 2, 3, 2, 1, 2, 3
];

const uniqueTechCount = new Set(PROJECTS.flatMap((project) => project.tags)).size;

export const GITHUB_SUMMARY: StatItem = {
  id: 'public-repos',
  label: 'Public Repo’s',
  value: '24',
  description: 'Mocked repository count for the portfolio dashboard.'
};

export const PORTFOLIO_STATS: StatItem[] = [
  {
    id: 'project-count',
    label: 'Total Projects',
    value: String(PROJECTS.length),
    description: 'Portfolio projects currently available in the mock dataset.'
  },
  {
    id: 'blog-count',
    label: 'Blog Posts',
    value: String(BLOG_POSTS.length),
    description: 'Published mock articles available for the blog listing.'
  },
  {
    id: 'tech-count',
    label: 'Tech Count',
    value: String(uniqueTechCount),
    description: 'Unique technologies currently referenced across project tags.',
    actionLabel: 'Love this portfolio'
  }
];
