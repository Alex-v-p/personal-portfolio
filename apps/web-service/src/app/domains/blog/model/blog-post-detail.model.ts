import { BlogPostSummary } from './blog-post-summary.model';

export interface BlogPostDetail extends BlogPostSummary {
  contentMarkdown: string;
  seoTitle?: string;
  seoDescription?: string;
}
