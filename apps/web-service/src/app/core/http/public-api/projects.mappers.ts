import { ResolvedMedia } from '@domains/media/model/resolved-media.model';
import { ProjectDetail } from '@domains/projects/model/project-detail.model';
import { ProjectLink, ProjectSummary } from '@domains/projects/model/project-summary.model';

import { normalizeMedia } from './common.mappers';
import { ProjectDetailApi, ProjectSummaryApi } from './projects.contracts';

export function normalizeProjectSummaries(items: ProjectSummaryApi[] | null | undefined): ProjectSummary[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((project) => normalizeProjectSummary(project));
}

export function normalizeProjectSummary(project: ProjectSummaryApi): ProjectSummary {
  const orderedSkills = [...(project.skills ?? [])].sort((left, right) => left.sortOrder - right.sortOrder || left.name.localeCompare(right.name));
  const coverImage = normalizeMedia(project.coverImage);
  const coverAlt = coverImage?.alt ?? project.title;
  const tags = orderedSkills.map((skill) => skill.name);
  const links: ProjectLink[] = [];

  if (project.githubUrl) {
    links.push({ label: 'GitHub', href: project.githubUrl });
  }

  if (project.demoUrl) {
    links.unshift({ label: 'Live Demo', href: project.demoUrl });
  }

  links.push({ label: 'Read more', routerLink: ['/projects', project.slug] });

  return {
    id: project.id,
    slug: project.slug,
    title: project.title,
    teaser: project.teaser,
    shortDescription: project.teaser,
    summary: project.summary ?? '',
    organization: project.companyName ?? '',
    duration: project.durationLabel,
    durationLabel: project.durationLabel,
    status: project.status,
    state: project.state,
    category: 'Project',
    tags,
    featured: project.isFeatured,
    isFeatured: project.isFeatured,
    imageAlt: coverAlt,
    coverImageAlt: coverAlt,
    coverImageFileId: project.coverImageFileId ?? null,
    coverImageUrl: coverImage?.url ?? undefined,
    highlight: project.summary ?? project.teaser,
    githubUrl: project.githubUrl ?? undefined,
    githubRepoName: project.githubRepoName ?? undefined,
    demoUrl: project.demoUrl ?? undefined,
    startedOn: project.startedOn ?? null,
    endedOn: project.endedOn ?? null,
    publishedAt: project.publishedAt ?? null,
    sortOrder: typeof project.sortOrder === 'number' ? project.sortOrder : Number.MAX_SAFE_INTEGER,
    links,
  };
}

export function normalizeProjectDetail(project: ProjectDetailApi): ProjectDetail {
  return {
    ...normalizeProjectSummary(project),
    descriptionMarkdown: project.descriptionMarkdown ?? undefined,
    images: (project.images ?? []).map((image) => normalizeMedia(image.image)).filter((item): item is ResolvedMedia => item !== null),
  };
}
