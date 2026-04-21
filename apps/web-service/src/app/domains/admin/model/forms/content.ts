import { AdminBlogPost, AdminExperience, AdminProject } from '@domains/admin/model/admin.model';

export interface AdminProjectForm {
  id?: string | null;
  slug: string;
  title: string;
  titleNl: string;
  teaser: string;
  teaserNl: string;
  summary: string;
  summaryNl: string;
  descriptionMarkdown: string;
  descriptionMarkdownNl: string;
  coverImageFileId: string | null;
  githubUrl: string;
  githubRepoOwner: string;
  githubRepoName: string;
  demoUrl: string;
  companyName: string;
  startedOn: string;
  endedOn: string;
  durationLabel: string;
  durationLabelNl: string;
  status: string;
  statusNl: string;
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
  titleNl: string;
  excerpt: string;
  excerptNl: string;
  contentMarkdown: string;
  contentMarkdownNl: string;
  coverImageFileId: string | null;
  coverImageAlt: string;
  coverImageAltNl: string;
  readingTimeMinutes: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt: string;
  seoTitle: string;
  seoTitleNl: string;
  seoDescription: string;
  seoDescriptionNl: string;
  tagIds: string[];
}

export interface AdminExperienceForm {
  id?: string | null;
  organizationName: string;
  roleTitle: string;
  roleTitleNl: string;
  location: string;
  experienceType: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
  summary: string;
  summaryNl: string;
  descriptionMarkdown: string;
  descriptionMarkdownNl: string;
  logoFileId: string | null;
  sortOrder: number;
  skillIds: string[];
}

export function createEmptyProjectForm(): AdminProjectForm {
  return {
    slug: '',
    title: '',
    titleNl: '',
    teaser: '',
    teaserNl: '',
    summary: '',
    summaryNl: '',
    descriptionMarkdown: '',
    descriptionMarkdownNl: '',
    coverImageFileId: null,
    githubUrl: '',
    githubRepoOwner: '',
    githubRepoName: '',
    demoUrl: '',
    companyName: '',
    startedOn: '',
    endedOn: '',
    durationLabel: '',
    durationLabelNl: '',
    status: '',
    statusNl: '',
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
    titleNl: '',
    excerpt: '',
    excerptNl: '',
    contentMarkdown: '',
    contentMarkdownNl: '',
    coverImageFileId: null,
    coverImageAlt: '',
    coverImageAltNl: '',
    readingTimeMinutes: null,
    status: 'draft',
    isFeatured: false,
    publishedAt: '',
    seoTitle: '',
    seoTitleNl: '',
    seoDescription: '',
    seoDescriptionNl: '',
    tagIds: []
  };
}

export function createEmptyExperienceForm(): AdminExperienceForm {
  return {
    organizationName: '',
    roleTitle: '',
    roleTitleNl: '',
    location: '',
    experienceType: 'work',
    startDate: '',
    endDate: '',
    isCurrent: false,
    summary: '',
    summaryNl: '',
    descriptionMarkdown: '',
    descriptionMarkdownNl: '',
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
    titleNl: project.titleNl ?? '',
    teaser: project.teaser,
    teaserNl: project.teaserNl ?? '',
    summary: project.summary ?? '',
    summaryNl: project.summaryNl ?? '',
    descriptionMarkdown: project.descriptionMarkdown ?? '',
    descriptionMarkdownNl: project.descriptionMarkdownNl ?? '',
    coverImageFileId: project.coverImageFileId ?? null,
    githubUrl: project.githubUrl ?? '',
    githubRepoOwner: project.githubRepoOwner ?? '',
    githubRepoName: project.githubRepoName ?? '',
    demoUrl: project.demoUrl ?? '',
    companyName: project.companyName ?? '',
    startedOn: project.startedOn ?? '',
    endedOn: project.endedOn ?? '',
    durationLabel: project.durationLabel,
    durationLabelNl: project.durationLabelNl ?? '',
    status: project.status,
    statusNl: project.statusNl ?? '',
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
    titleNl: post.titleNl ?? '',
    excerpt: post.excerpt,
    excerptNl: post.excerptNl ?? '',
    contentMarkdown: post.contentMarkdown,
    contentMarkdownNl: post.contentMarkdownNl ?? '',
    coverImageFileId: post.coverImageFileId ?? null,
    coverImageAlt: post.coverImageAlt ?? '',
    coverImageAltNl: post.coverImageAltNl ?? '',
    readingTimeMinutes: post.readingTimeMinutes ?? null,
    status: post.status,
    isFeatured: post.isFeatured,
    publishedAt: post.publishedAt?.slice(0, 16) ?? '',
    seoTitle: post.seoTitle ?? '',
    seoTitleNl: post.seoTitleNl ?? '',
    seoDescription: post.seoDescription ?? '',
    seoDescriptionNl: post.seoDescriptionNl ?? '',
    tagIds: [...post.tagIds],
  };
}

export function toExperienceForm(experience: AdminExperience): AdminExperienceForm {
  return {
    id: experience.id,
    organizationName: experience.organizationName,
    roleTitle: experience.roleTitle,
    roleTitleNl: experience.roleTitleNl ?? '',
    location: experience.location ?? '',
    experienceType: experience.experienceType,
    startDate: experience.startDate,
    endDate: experience.endDate ?? '',
    isCurrent: experience.isCurrent,
    summary: experience.summary,
    summaryNl: experience.summaryNl ?? '',
    descriptionMarkdown: experience.descriptionMarkdown ?? '',
    descriptionMarkdownNl: experience.descriptionMarkdownNl ?? '',
    logoFileId: experience.logoFileId ?? null,
    sortOrder: experience.sortOrder,
    skillIds: [...experience.skillIds],
  };
}
