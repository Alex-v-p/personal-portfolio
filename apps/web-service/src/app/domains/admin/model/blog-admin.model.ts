import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { AdminBlogTag } from './taxonomy-admin.model';

export interface AdminProtectedDocument {
  id: string;
  mediaFileId: string;
  title?: string | null;
  titleNl?: string | null;
  sortOrder: number;
  media?: ResolvedMedia | null;
}

export interface AdminProtectedDocumentGroup {
  id: string;
  slug: string;
  title: string;
  titleNl?: string | null;
  description?: string | null;
  descriptionNl?: string | null;
  isEnabled: boolean;
  sortOrder: number;
  hasPassword: boolean;
  documents: AdminProtectedDocument[];
}

export interface AdminProtectedDocumentUpsert {
  id?: string | null;
  mediaFileId?: string | null;
  title?: string | null;
  titleNl?: string | null;
  sortOrder: number;
}

export interface AdminProtectedDocumentGroupUpsert {
  id?: string | null;
  slug?: string | null;
  title: string;
  titleNl?: string | null;
  description?: string | null;
  descriptionNl?: string | null;
  isEnabled: boolean;
  sortOrder: number;
  newPassword?: string | null;
  documents: AdminProtectedDocumentUpsert[];
}

export interface AdminBlogPost {
  id: string;
  slug: string;
  title: string;
  titleNl?: string | null;
  excerpt: string;
  excerptNl?: string | null;
  contentMarkdown: string;
  contentMarkdownNl?: string | null;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  coverImageAltNl?: string | null;
  coverImage?: ResolvedMedia | null;
  readingTimeMinutes?: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt?: string | null;
  seoTitle?: string | null;
  seoTitleNl?: string | null;
  seoDescription?: string | null;
  seoDescriptionNl?: string | null;
  createdAt: string;
  updatedAt: string;
  tagIds: string[];
  tagNames: string[];
  tags: AdminBlogTag[];
  protectedDocumentGroups: AdminProtectedDocumentGroup[];
}

export interface AdminBlogPostUpsert {
  slug?: string | null;
  title: string;
  titleNl?: string | null;
  excerpt: string;
  excerptNl?: string | null;
  contentMarkdown: string;
  contentMarkdownNl?: string | null;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  coverImageAltNl?: string | null;
  readingTimeMinutes?: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt?: string | null;
  seoTitle?: string | null;
  seoTitleNl?: string | null;
  seoDescription?: string | null;
  seoDescriptionNl?: string | null;
  tagIds: string[];
  protectedDocumentGroups: AdminProtectedDocumentGroupUpsert[];
}
