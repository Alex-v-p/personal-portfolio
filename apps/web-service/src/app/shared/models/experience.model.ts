export interface Experience {
  id: string;
  organizationName: string;
  roleTitle: string;
  title: string;
  organization: string;
  location: string;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  period: string;
  summary: string;
  descriptionMarkdown?: string;
  logoFileId?: string | null;
  logoUrl?: string;
  sortOrder: number;
}
