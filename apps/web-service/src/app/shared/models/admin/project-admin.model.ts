import { ResolvedMedia } from '../resolved-media.model';
import { AdminSkillOption } from './taxonomy-admin.model';

export interface AdminProject {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  summary?: string | null;
  descriptionMarkdown?: string | null;
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
  status: string;
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
  teaser: string;
  summary?: string | null;
  descriptionMarkdown?: string | null;
  coverImageFileId?: string | null;
  githubUrl?: string | null;
  githubRepoOwner?: string | null;
  githubRepoName?: string | null;
  demoUrl?: string | null;
  companyName?: string | null;
  startedOn?: string | null;
  endedOn?: string | null;
  durationLabel: string;
  status: string;
  state: 'published' | 'archived' | 'completed' | 'paused';
  isFeatured: boolean;
  sortOrder: number;
  publishedAt?: string | null;
  skillIds: string[];
}
