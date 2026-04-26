import { ProjectState } from '@domains/projects/model/project-summary.model';

import { MediaApi, SkillApi } from './common.contracts';

export interface ProjectImageApi {
  id: string;
  projectId: string;
  imageFileId?: string | null;
  altText?: string | null;
  sortOrder: number;
  isCover: boolean;
  image?: MediaApi | null;
}

export interface ProjectSummaryApi {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  summary?: string | null;
  coverImageFileId?: string | null;
  coverImage?: MediaApi | null;
  githubUrl?: string | null;
  githubRepoOwner?: string | null;
  githubRepoName?: string | null;
  demoUrl?: string | null;
  companyName?: string | null;
  startedOn?: string | null;
  endedOn?: string | null;
  durationLabel: string;
  status: string;
  state: ProjectState;
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  createdAt: string;
  updatedAt: string;
  skills: SkillApi[];
  images?: ProjectImageApi[] | null;
}

export interface ProjectDetailApi extends ProjectSummaryApi {
  descriptionMarkdown?: string | null;
  images: ProjectImageApi[];
}
