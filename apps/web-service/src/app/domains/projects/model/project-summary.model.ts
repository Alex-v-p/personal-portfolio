import { ResolvedMedia } from '@domains/media/model/resolved-media.model';

export interface ProjectLink {
  label: string;
  href?: string;
  routerLink?: string | readonly string[];
}

export type ProjectState = 'published' | 'archived' | 'completed' | 'paused';

export interface ProjectSummary {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  shortDescription: string;
  summary: string;
  organization: string;
  duration: string;
  durationLabel: string;
  status: string;
  state: ProjectState;
  category: string;
  tags: string[];
  featured: boolean;
  isFeatured: boolean;
  imageAlt: string;
  coverImageAlt: string;
  coverImageFileId?: string | null;
  coverImageUrl?: string;
  galleryImages: ResolvedMedia[];
  highlight: string;
  githubUrl?: string;
  githubRepoName?: string;
  demoUrl?: string;
  startedOn?: string | null;
  endedOn?: string | null;
  publishedAt?: string | null;
  sortOrder: number;
  links: ProjectLink[];
}
