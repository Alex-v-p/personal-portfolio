import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { AdminSkillOption } from './taxonomy-admin.model';

export interface AdminExperience {
  id: string;
  organizationName: string;
  roleTitle: string;
  roleTitleNl?: string | null;
  location?: string | null;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  summary: string;
  summaryNl?: string | null;
  descriptionMarkdown?: string | null;
  descriptionMarkdownNl?: string | null;
  logoFileId?: string | null;
  logo?: ResolvedMedia | null;
  sortOrder: number;
  createdAt: string;
  updatedAt: string;
  skillIds: string[];
  skills: AdminSkillOption[];
}

export interface AdminExperienceUpsert {
  organizationName: string;
  roleTitle: string;
  roleTitleNl?: string | null;
  location?: string | null;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  summary: string;
  summaryNl?: string | null;
  descriptionMarkdown?: string | null;
  descriptionMarkdownNl?: string | null;
  logoFileId?: string | null;
  sortOrder: number;
  skillIds: string[];
}
