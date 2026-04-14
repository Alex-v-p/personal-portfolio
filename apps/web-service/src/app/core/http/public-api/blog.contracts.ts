import { BlogPostStatus } from '@domains/blog/model/blog-post-summary.model';

import { MediaApi } from './common.contracts';

export interface BlogTagApi {
  id: string;
  name: string;
  slug: string;
}

export interface BlogPostSummaryApi {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  coverImage?: MediaApi | null;
  readingTimeMinutes?: number | null;
  status: BlogPostStatus;
  isFeatured: boolean;
  publishedAt?: string | null;
  createdAt: string;
  updatedAt: string;
  tags: BlogTagApi[];
}

export interface BlogPostDetailApi extends BlogPostSummaryApi {
  contentMarkdown: string;
  seoTitle?: string | null;
  seoDescription?: string | null;
}
