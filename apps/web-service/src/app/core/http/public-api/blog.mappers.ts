import { AppLocale } from '@core/i18n/locales';
import { BlogPostDetail } from '@domains/blog/model/blog-post-detail.model';
import { BlogPostSummary } from '@domains/blog/model/blog-post-summary.model';
import { ProtectedDocument, ProtectedDocumentGroup } from '@domains/blog/model/protected-document.model';

import { formatDate, normalizeMedia, readingTimeLabel } from './common.mappers';
import { BlogPostDetailApi, BlogPostSummaryApi, ProtectedDocumentApi, ProtectedDocumentGroupApi } from './blog.contracts';


export function normalizeProtectedDocumentGroups(items: ProtectedDocumentGroupApi[] | null | undefined): ProtectedDocumentGroup[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items
    .map((group) => ({
      slug: group.slug,
      title: group.title,
      description: group.description ?? undefined,
      documents: normalizeProtectedDocuments(group.documents),
    }))
    .filter((group) => group.slug && group.documents.length > 0);
}

function normalizeProtectedDocuments(items: ProtectedDocumentApi[] | null | undefined): ProtectedDocument[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items
    .map((document) => ({
      id: document.id,
      title: document.title,
      fileName: document.fileName ?? undefined,
      mimeType: document.mimeType ?? undefined,
      fileSizeBytes: typeof document.fileSizeBytes === 'number' ? document.fileSizeBytes : undefined,
      downloadUrl: document.downloadUrl,
    }))
    .filter((document) => document.id && document.downloadUrl);
}

export function normalizeBlogPostSummaries(items: BlogPostSummaryApi[] | null | undefined, locale: AppLocale): BlogPostSummary[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((post) => normalizeBlogPostSummary(post, locale));
}

export function normalizeBlogPostSummary(post: BlogPostSummaryApi, locale: AppLocale): BlogPostSummary {
  const tagNames = Array.isArray(post.tags) ? post.tags.map((tag) => tag.name) : [];
  const readingTimeMinutes = typeof post.readingTimeMinutes === 'number' ? post.readingTimeMinutes : 0;
  const cover = normalizeMedia(post.coverImage);
  const coverAlt = cover?.alt ?? post.coverImageAlt ?? (locale === 'nl' ? 'Tijdelijke blogafbeelding' : 'Blog post cover placeholder');

  return {
    id: post.id,
    slug: post.slug,
    title: post.title,
    excerpt: post.excerpt ?? '',
    publishedAt: formatDate(post.publishedAt, locale),
    readTime: readingTimeLabel(readingTimeMinutes, locale),
    readingTimeMinutes,
    category: tagNames[0] ?? (locale === 'nl' ? 'Algemeen' : 'General'),
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

export function normalizeBlogPostDetail(post: BlogPostDetailApi, locale: AppLocale): BlogPostDetail {
  return {
    ...normalizeBlogPostSummary(post, locale),
    contentMarkdown: post.contentMarkdown ?? '',
    seoTitle: post.seoTitle ?? undefined,
    seoDescription: post.seoDescription ?? undefined,
    protectedDocumentGroups: normalizeProtectedDocumentGroups(post.protectedDocumentGroups),
  };
}
