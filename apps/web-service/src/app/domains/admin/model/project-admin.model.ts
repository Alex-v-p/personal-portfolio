import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { AdminSkillOption } from './taxonomy-admin.model';

export interface AdminProject {
  id: string;
  slug: string;
  title: string;
  titleNl?: string | null;
  teaser: string;
  teaserNl?: string | null;
  summary?: string | null;
  summaryNl?: string | null;
  descriptionMarkdown?: string | null;
  descriptionMarkdownNl?: string | null;
  coverImageFileId?: string | null;
  coverImage?: ResolvedMedia | null;
  githubUrl?: string | null;
  githubRepoOwner?: string | null;
  githubRepoName?: string | null;
  demoUrl?: string | null;
  companyName?: string | null;
  startedOn?: string | null;
  endedOn?: string | null;
  durationLabel: string;
  durationLabelNl?: string | null;
  status: string;
  statusNl?: string | null;
  state: 'published' | 'archived' | 'completed' | 'paused';
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  createdAt: string;
  updatedAt: string;
  skillIds: string[];
  skills: AdminSkillOption[];
}

export interface AdminProjectUpsert {
  slug?: string | null;
  title: string;
  titleNl?: string | null;
  teaser: string;
  teaserNl?: string | null;
  summary?: string | null;
  summaryNl?: string | null;
  descriptionMarkdown?: string | null;
  descriptionMarkdownNl?: string | null;
  coverImageFileId?: string | null;
  githubUrl?: string | null;
  githubRepoOwner?: string | null;
  githubRepoName?: string | null;
  demoUrl?: string | null;
  companyName?: string | null;
  startedOn?: string | null;
  endedOn?: string | null;
  durationLabel: string;
  durationLabelNl?: string | null;
  status: string;
  statusNl?: string | null;
  state: 'published' | 'archived' | 'completed' | 'paused';
  isFeatured: boolean;
  sortOrder: number;
  publishedAt?: string | null;
  skillIds: string[];
}
