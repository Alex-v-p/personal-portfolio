import { Experience } from '@domains/experience/model/experience.model';

import { formatPeriod, normalizeMedia } from './common.mappers';
import { ExperienceApi } from './experience.contracts';

export function normalizeExperienceList(items: ExperienceApi[] | null | undefined): Experience[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((item) => normalizeExperience(item));
}

export function normalizeExperience(item: ExperienceApi): Experience {
  const title = item.roleTitle;
  const organization = item.organizationName;
  const location = item.location ?? '';

  return {
    id: item.id,
    organizationName: organization,
    roleTitle: title,
    title,
    organization,
    location,
    experienceType: item.experienceType,
    startDate: item.startDate,
    endDate: item.endDate ?? null,
    isCurrent: item.isCurrent,
    period: formatPeriod(item.startDate, item.endDate, item.isCurrent),
    summary: item.summary,
    descriptionMarkdown: item.descriptionMarkdown ?? undefined,
    logoFileId: item.logoFileId ?? null,
    logoUrl: normalizeMedia(item.logo)?.url ?? undefined,
    sortOrder: item.sortOrder,
    skillNames: Array.isArray(item.skillNames) ? item.skillNames : [],
  };
}
