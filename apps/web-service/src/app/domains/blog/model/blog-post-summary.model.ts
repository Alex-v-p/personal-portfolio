export type BlogPostStatus = 'draft' | 'published' | 'archived';

export interface BlogPostSummary {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  publishedAt: string;
  readTime: string;
  readingTimeMinutes: number;
  category: string;
  tags: string[];
  featured: boolean;
  isFeatured: boolean;
  coverAlt: string;
  coverImageAlt: string;
  coverImageFileId?: string | null;
  coverImageUrl?: string;
  status: BlogPostStatus;
}
