import { AdminBlogPost, AdminExperience, AdminProject } from '@domains/admin/model/admin.model';

export interface AdminProjectForm {
  id?: string | null;
  slug: string;
  title: string;
  teaser: string;
  summary: string;
  descriptionMarkdown: string;
  coverImageFileId: string | null;
  githubUrl: string;
  githubRepoOwner: string;
  githubRepoName: string;
  demoUrl: string;
  companyName: string;
  startedOn: string;
  endedOn: string;
  durationLabel: string;
  status: string;
  state: 'published' | 'archived' | 'completed' | 'paused';
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  skillIds: string[];
}

export interface AdminBlogPostForm {
  id?: string | null;
  slug: string;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId: string | null;
  coverImageAlt: string;
  readingTimeMinutes: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt: string;
  seoTitle: string;
  seoDescription: string;
  tagIds: string[];
}

export interface AdminExperienceForm {
  id?: string | null;
  organizationName: string;
  roleTitle: string;
  location: string;
  experienceType: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown: string;
  logoFileId: string | null;
  sortOrder: number;
  skillIds: string[];
}

export function createEmptyProjectForm(): AdminProjectForm {
  return {
    slug: '',
    title: '',
    teaser: '',
    summary: '',
    descriptionMarkdown: '',
    coverImageFileId: null,
    githubUrl: '',
    githubRepoOwner: '',
    githubRepoName: '',
    demoUrl: '',
    companyName: '',
    startedOn: '',
    endedOn: '',
    durationLabel: '',
    status: '',
    state: 'published',
    isFeatured: false,
    sortOrder: 0,
    publishedAt: '',
    skillIds: []
  };
}

export function createEmptyBlogPostForm(): AdminBlogPostForm {
  return {
    slug: '',
    title: '',
    excerpt: '',
    contentMarkdown: '',
    coverImageFileId: null,
    coverImageAlt: '',
    readingTimeMinutes: null,
    status: 'draft',
    isFeatured: false,
    publishedAt: '',
    seoTitle: '',
    seoDescription: '',
    tagIds: []
  };
}

export function createEmptyExperienceForm(): AdminExperienceForm {
  return {
    organizationName: '',
    roleTitle: '',
    location: '',
    experienceType: 'work',
    startDate: '',
    endDate: '',
    isCurrent: false,
    summary: '',
    descriptionMarkdown: '',
    logoFileId: null,
    sortOrder: 0,
    skillIds: []
  };
}

export function toProjectForm(project: AdminProject): AdminProjectForm {
  return {
    id: project.id,
    slug: project.slug,
    title: project.title,
    teaser: project.teaser,
    summary: project.summary ?? '',
    descriptionMarkdown: project.descriptionMarkdown ?? '',
    coverImageFileId: project.coverImageFileId ?? null,
    githubUrl: project.githubUrl ?? '',
    githubRepoOwner: project.githubRepoOwner ?? '',
    githubRepoName: project.githubRepoName ?? '',
    demoUrl: project.demoUrl ?? '',
    companyName: project.companyName ?? '',
    startedOn: project.startedOn ?? '',
    endedOn: project.endedOn ?? '',
    durationLabel: project.durationLabel,
    status: project.status,
    state: project.state,
    isFeatured: project.isFeatured,
    sortOrder: project.sortOrder,
    publishedAt: project.publishedAt?.slice(0, 16) ?? '',
    skillIds: [...project.skillIds],
  };
}

export function toBlogPostForm(post: AdminBlogPost): AdminBlogPostForm {
  return {
    id: post.id,
    slug: post.slug,
    title: post.title,
    excerpt: post.excerpt,
    contentMarkdown: post.contentMarkdown,
    coverImageFileId: post.coverImageFileId ?? null,
    coverImageAlt: post.coverImageAlt ?? '',
    readingTimeMinutes: post.readingTimeMinutes ?? null,
    status: post.status,
    isFeatured: post.isFeatured,
    publishedAt: post.publishedAt?.slice(0, 16) ?? '',
    seoTitle: post.seoTitle ?? '',
    seoDescription: post.seoDescription ?? '',
    tagIds: [...post.tagIds],
  };
}

export function toExperienceForm(experience: AdminExperience): AdminExperienceForm {
  return {
    id: experience.id,
    organizationName: experience.organizationName,
    roleTitle: experience.roleTitle,
    location: experience.location ?? '',
    experienceType: experience.experienceType,
    startDate: experience.startDate,
    endDate: experience.endDate ?? '',
    isCurrent: experience.isCurrent,
    summary: experience.summary,
    descriptionMarkdown: experience.descriptionMarkdown ?? '',
    logoFileId: experience.logoFileId ?? null,
    sortOrder: experience.sortOrder,
    skillIds: [...experience.skillIds],
  };
}
