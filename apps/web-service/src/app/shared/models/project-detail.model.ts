import { ResolvedMedia } from './resolved-media.model';
import { ProjectSummary } from './project-summary.model';

export interface ProjectDetail extends ProjectSummary {
  descriptionMarkdown?: string;
  images: ResolvedMedia[];
}
