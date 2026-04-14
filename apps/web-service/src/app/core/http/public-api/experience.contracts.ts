import { MediaApi } from './common.contracts';

export interface ExperienceApi {
  id: string;
  organizationName: string;
  roleTitle: string;
  location?: string | null;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown?: string | null;
  logoFileId?: string | null;
  logo?: MediaApi | null;
  sortOrder: number;
  skillNames: string[];
  createdAt: string;
  updatedAt: string;
}
