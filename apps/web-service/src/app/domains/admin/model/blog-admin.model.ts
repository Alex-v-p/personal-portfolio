import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { AdminBlogTag } from './taxonomy-admin.model';

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
}
