import { ResolvedMedia } from './resolved-media.model';

export interface AdminUser {
  id: string;
  email: string;
  displayName: string;
  isActive: boolean;
  createdAt: string;
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

export interface AdminSkillOption {
  id: string;
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
  tagNames: string[];
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
  mediaFiles: AdminMediaFile[];
  blogTags: AdminBlogTag[];
  projectStates: Array<'published' | 'archived' | 'completed' | 'paused'>;
  publicationStatuses: Array<'draft' | 'published' | 'archived'>;
}

export interface AdminDashboardSummary {
  projects: number;
  blogPosts: number;
  unreadMessages: number;
  skills: number;
  mediaFiles: number;
}

export interface AdminCollectionResponse<T> {
  items: T[];
  total: number;
}
