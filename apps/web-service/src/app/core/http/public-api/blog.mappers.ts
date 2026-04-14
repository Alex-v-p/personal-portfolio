import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';

import { formatDate, normalizeMedia } from './common.mappers';
import { BlogPostDetailApi, BlogPostSummaryApi } from './blog.contracts';

export function normalizeBlogPostSummaries(items: BlogPostSummaryApi[] | null | undefined): BlogPostSummary[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((post) => normalizeBlogPostSummary(post));
}

export function normalizeBlogPostSummary(post: BlogPostSummaryApi): BlogPostSummary {
  const tagNames = Array.isArray(post.tags) ? post.tags.map((tag) => tag.name) : [];
  const readingTimeMinutes = typeof post.readingTimeMinutes === 'number' ? post.readingTimeMinutes : 0;
  const cover = normalizeMedia(post.coverImage);
  const coverAlt = cover?.alt ?? post.coverImageAlt ?? 'Blog post cover placeholder';

  return {
    id: post.id,
    slug: post.slug,
    title: post.title,
    excerpt: post.excerpt ?? '',
    publishedAt: formatDate(post.publishedAt),
    readTime: readingTimeMinutes > 0 ? `${readingTimeMinutes} min read` : 'Draft',
    readingTimeMinutes,
    category: tagNames[0] ?? 'General',
    tags: tagNames,
    featured: post.isFeatured,
    isFeatured: post.isFeatured,
    coverAlt,
    coverImageAlt: coverAlt,
    coverImageFileId: post.coverImageFileId ?? null,
    coverImageUrl: cover?.url ?? undefined,
    status: post.status,
  };
}

export function normalizeBlogPostDetail(post: BlogPostDetailApi): BlogPostDetail {
  return {
    ...normalizeBlogPostSummary(post),
    contentMarkdown: post.contentMarkdown ?? '',
    seoTitle: post.seoTitle ?? undefined,
    seoDescription: post.seoDescription ?? undefined,
  };
}
