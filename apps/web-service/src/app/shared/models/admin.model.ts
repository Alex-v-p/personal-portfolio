import { ResolvedMedia } from './resolved-media.model';

export interface AdminUser {
  id: string;
  email: string;
  displayName: string;
  isActive: boolean;
  createdAt: string;
}

export interface AdminUserCreate {
  email: string;
  displayName: string;
  password: string;
  isActive: boolean;
}

export interface AdminUserUpdate {
  email: string;
  displayName: string;
  password?: string | null;
  isActive: boolean;
}

export interface AdminAuthToken {
  accessToken: string;
  tokenType: string;
  expiresInSeconds: number;
  user: AdminUser;
}

export interface AdminMediaFile {
  id: string;
  bucketName: string;
  objectKey: string;
  originalFilename: string;
  mimeType?: string | null;
  visibility: string;
  altText?: string | null;
  title?: string | null;
  publicUrl?: string | null;
  resolvedAsset?: ResolvedMedia | null;
  createdAt: string;
  updatedAt: string;
}

export interface AdminSkillCategory {
  id: string;
  name: string;
  description?: string | null;
  sortOrder: number;
}

export interface AdminSkillCategoryUpsert {
  name: string;
  description?: string | null;
  sortOrder: number;
}

export interface AdminSkillOption {
  id: string;
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface AdminSkillUpsert {
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

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

export interface AdminBlogTag {
  id: string;
  name: string;
  slug: string;
}

export interface AdminBlogTagUpsert {
  name: string;
  slug?: string | null;
}

export interface AdminBlogPost {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  coverImage?: ResolvedMedia | null;
  readingTimeMinutes?: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt?: string | null;
  seoTitle?: string | null;
  seoDescription?: string | null;
  createdAt: string;
  updatedAt: string;
  tagIds: string[];
  tagNames: string[];
  tags: AdminBlogTag[];
}

export interface AdminBlogPostUpsert {
  slug?: string | null;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  readingTimeMinutes?: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt?: string | null;
  seoTitle?: string | null;
  seoDescription?: string | null;
  tagIds: string[];
}

export interface AdminSocialLink {
  id?: string | null;
  platform: string;
  label: string;
  url: string;
  iconKey?: string | null;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminProfile {
  id: string;
  firstName: string;
  lastName: string;
  headline: string;
  shortIntro: string;
  longBio?: string | null;
  location?: string | null;
  email?: string | null;
  phone?: string | null;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  avatar?: ResolvedMedia | null;
  heroImage?: ResolvedMedia | null;
  resume?: ResolvedMedia | null;
  ctaPrimaryLabel?: string | null;
  ctaPrimaryUrl?: string | null;
  ctaSecondaryLabel?: string | null;
  ctaSecondaryUrl?: string | null;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
  createdAt: string;
  updatedAt: string;
}

export interface AdminProfileUpdate {
  firstName: string;
  lastName: string;
  headline: string;
  shortIntro: string;
  longBio?: string | null;
  location?: string | null;
  email?: string | null;
  phone?: string | null;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  ctaPrimaryLabel?: string | null;
  ctaPrimaryUrl?: string | null;
  ctaSecondaryLabel?: string | null;
  ctaSecondaryUrl?: string | null;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
}

export interface AdminExperience {
  id: string;
  organizationName: string;
  roleTitle: string;
  location?: string | null;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown?: string | null;
  logoFileId?: string | null;
  logo?: ResolvedMedia | null;
  sortOrder: number;
  createdAt: string;
  updatedAt: string;
  skillIds: string[];
  skills: AdminSkillOption[];
}

export interface AdminExperienceUpsert {
  organizationName: string;
  roleTitle: string;
  location?: string | null;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown?: string | null;
  logoFileId?: string | null;
  sortOrder: number;
  skillIds: string[];
}

export interface AdminNavigationItem {
  id: string;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminNavigationItemUpsert {
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminGithubContributionDay {
  date: string;
  count: number;
  level: number;
}

export interface AdminGithubSnapshot {
  id: string;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount?: number | null;
  followingCount?: number | null;
  totalStars?: number | null;
  totalCommits?: number | null;
  rawPayload?: Record<string, unknown> | null;
  contributionDays: AdminGithubContributionDay[];
  createdAt: string;
  updatedAt: string;
}

export interface AdminGithubSnapshotUpsert {
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount?: number | null;
  followingCount?: number | null;
  totalStars?: number | null;
  totalCommits?: number | null;
  rawPayload?: Record<string, unknown> | null;
  contributionDays: AdminGithubContributionDay[];
}

export interface AdminGithubSnapshotRefreshRequest {
  username?: string | null;
  pruneHistory: boolean;
}

export interface AdminContactMessage {
  id: string;
  name: string;
  email: string;
  subject: string;
  message: string;
  sourcePage: string;
  isRead: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AdminReferenceData {
  skills: AdminSkillOption[];
  skillCategories: AdminSkillCategory[];
  mediaFiles: AdminMediaFile[];
  blogTags: AdminBlogTag[];
  projectStates: Array<'published' | 'archived' | 'completed' | 'paused'>;
  publicationStatuses: Array<'draft' | 'published' | 'archived'>;
}


export interface AdminAssistantKnowledgeStatus {
  totalDocuments: number;
  totalChunks: number;
  documentsBySourceType: Record<string, number>;
  latestUpdatedAt?: string | null;
}

export interface AdminDashboardSummary {
  projects: number;
  blogPosts: number;
  unreadMessages: number;
  skills: number;
  skillCategories: number;
  mediaFiles: number;
  experiences: number;
  navigationItems: number;
  blogTags: number;
  adminUsers: number;
  githubSnapshots: number;
}

export interface AdminCollectionResponse<T> {
  items: T[];
  total: number;
}
