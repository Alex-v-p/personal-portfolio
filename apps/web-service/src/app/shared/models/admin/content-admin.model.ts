import { ResolvedMedia } from '../resolved-media.model';
import { AdminBlogTag, AdminSkillOption } from './taxonomy-admin.model';

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
