import { BlogPostSummary } from './blog-post-summary.model';
import { ProtectedDocumentGroup } from './protected-document.model';

export interface BlogPostDetail extends BlogPostSummary {
  contentMarkdown: string;
  seoTitle?: string;
  seoDescription?: string;
  protectedDocumentGroups: ProtectedDocumentGroup[];
}
