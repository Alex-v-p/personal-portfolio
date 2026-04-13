import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { AdminBlogTag } from './taxonomy-admin.model';

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
