import { BlogPostDetail } from '../../models/blog-post-detail.model';
import { BlogPostSummary } from '../../models/blog-post-summary.model';
import { ContactMethod } from '../../models/contact-method.model';
import { Experience } from '../../models/experience.model';
import { GithubSnapshot } from '../../models/github-snapshot.model';
import { HomePageData } from '../../models/home.model';
import { Profile } from '../../models/profile.model';
import { ProjectDetail } from '../../models/project-detail.model';
import { ProjectLink, ProjectSummary } from '../../models/project-summary.model';
import { ResolvedMedia } from '../../models/resolved-media.model';
import { NavigationItem, SiteShellData } from '../../models/site-shell.model';
import { SocialLink } from '../../models/social-link.model';
import { StatItem } from '../../models/stat-item.model';
import { StatsPageData } from '../../models/stats-page.model';
import {
  BlogPostDetailApi,
  BlogPostSummaryApi,
  ContactMethodApi,
  ExperienceApi,
  GithubSnapshotApi,
  HomeApi,
  MediaApi,
  NavigationItemApi,
  ProfileApi,
  ProjectDetailApi,
  ProjectSummaryApi,
  SiteShellApi,
  SocialLinkApi,
  StatItemApi,
  StatsApi,
} from './public-api.contracts';

export function normalizeNavigationItem(item: NavigationItemApi): NavigationItem {
  return {
    id: item.id,
    label: item.label,
    routePath: item.routePath,
    isExternal: item.isExternal,
    sortOrder: item.sortOrder,
    isVisible: item.isVisible,
  };
}

export function normalizeProfile(profile: ProfileApi): Profile {
  const fullName = [profile.firstName, profile.lastName].filter(Boolean).join(' ').trim();
  const longBio = profile.longBio ?? '';
  const shortIntro = profile.shortIntro ?? '';
  const headline = profile.headline ?? 'Portfolio Builder';
  const socialLinks = normalizeSocialLinks(profile.socialLinks);
  const heroActions = [
    toHeroAction(profile.ctaPrimaryLabel, profile.ctaPrimaryUrl, 'primary'),
    toHeroAction(profile.ctaSecondaryLabel, profile.ctaSecondaryUrl, 'secondary')
  ].filter((action): action is Profile['heroActions'][number] => action !== null);

  return {
    id: profile.id,
    firstName: profile.firstName,
    lastName: profile.lastName,
    name: fullName,
    headline,
    role: headline,
    greeting: `Hi, I'm ${profile.firstName}`,
    location: profile.location ?? '',
    email: profile.email ?? '',
    phone: profile.phone ?? '',
    shortIntro,
    longBio,
    heroTitle: `I’m ${headline}`,
    summary: shortIntro || longBio,
    shortBio: longBio || shortIntro,
    footerDescription: profile.footerDescription || longBio || shortIntro,
    avatarFileId: profile.avatarFileId ?? null,
    heroImageFileId: profile.heroImageFileId ?? null,
    resumeFileId: profile.resumeFileId ?? null,
    avatarUrl: normalizeMedia(profile.avatar)?.url ?? '',
    heroImageUrl: normalizeMedia(profile.heroImage)?.url ?? '',
    resumeUrl: normalizeMedia(profile.resume)?.url ?? '',
    skills: Array.isArray(profile.skills) ? profile.skills : [],
    expertiseGroups: Array.isArray(profile.expertiseGroups) ? profile.expertiseGroups : [],
    introParagraphs: Array.isArray(profile.introParagraphs) ? profile.introParagraphs : [shortIntro, longBio].filter(Boolean),
    availability: Array.isArray(profile.availability) ? profile.availability : [],
    heroActions,
    socialLinks,
    createdAt: profile.createdAt,
    updatedAt: profile.updatedAt,
  };
}

export function normalizeSiteShell(shell: SiteShellApi): SiteShellData {
  return {
    navigation: (shell.navigation.items ?? []).map((item) => normalizeNavigationItem(item)),
    profile: normalizeProfile(shell.profile),
    footerText: shell.footerText ?? '',
    contactMethods: normalizeContactMethods(shell.contactMethods),
  };
}

export function normalizeHome(home: HomeApi): HomePageData {
  return {
    hero: normalizeProfile(home.hero),
    featuredProjects: normalizeProjectSummaries(home.featuredProjects),
    featuredBlogPosts: normalizeBlogPostSummaries(home.featuredBlogPosts),
    expertiseGroups: home.expertiseGroups ?? [],
    experiencePreview: normalizeExperienceList(home.experiencePreview),
    contactPreview: normalizeContactMethods(home.contactPreview),
  };
}

export function normalizeMedia(media: MediaApi | null | undefined): ResolvedMedia | null {
  if (!media?.url) {
    return null;
  }

  return {
    id: media.id,
    url: media.url,
    alt: media.alt ?? null,
    fileName: media.fileName ?? null,
    mimeType: media.mimeType ?? null,
    width: media.width ?? null,
    height: media.height ?? null,
  };
}

export function normalizeSocialLinks(items: SocialLinkApi[] | null | undefined): SocialLink[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((link) => ({
    id: link.id,
    profileId: link.profileId,
    platform: link.platform,
    label: link.label,
    url: link.url,
    iconKey: link.iconKey ?? '',
    sortOrder: link.sortOrder,
    isVisible: link.isVisible,
  }));
}

export function normalizeContactMethods(items: ContactMethodApi[] | null | undefined): ContactMethod[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((item) => ({
    id: item.id,
    platform: item.platform,
    label: item.label,
    value: item.value,
    href: item.href,
    actionLabel: item.actionLabel,
    iconKey: item.iconKey ?? undefined,
    description: item.description ?? undefined,
    sortOrder: item.sortOrder,
    isVisible: item.isVisible,
  }));
}

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

export function normalizeBlogPostSummaries(items: BlogPostSummaryApi[] | null | undefined): BlogPostSummary[] {
  if (!Array.isArray(items)) {
    return [];
  }

  return items.map((post) => normalizeBlogPostSummary(post));
}

export function normalizeBlogPostSummary(post: BlogPostSummaryApi): BlogPostSummary {
  const tagNames = Array.isArray(post.tags) ? post.tags.map((tag) => tag.name) : [];
  const readingTimeMinutes = typeof post.readingTimeMinutes === 'number' ? post.readingTimeMinutes : 0;
  const cover = normalizeMedia(post.coverImage);
  const coverAlt = cover?.alt ?? post.coverImageAlt ?? 'Blog post cover placeholder';

  return {
    id: post.id,
    slug: post.slug,
    title: post.title,
    excerpt: post.excerpt ?? '',
    publishedAt: formatDate(post.publishedAt),
    readTime: readingTimeMinutes > 0 ? `${readingTimeMinutes} min read` : 'Draft',
    readingTimeMinutes,
    category: tagNames[0] ?? 'General',
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

export function normalizeBlogPostDetail(post: BlogPostDetailApi): BlogPostDetail {
  return {
    ...normalizeBlogPostSummary(post),
    contentMarkdown: post.contentMarkdown ?? '',
    seoTitle: post.seoTitle ?? undefined,
    seoDescription: post.seoDescription ?? undefined,
  };
}

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

export function normalizeGithubSnapshot(snapshot: GithubSnapshotApi): GithubSnapshot {
  return {
    id: snapshot.id,
    snapshotDate: snapshot.snapshotDate,
    username: snapshot.username,
    publicRepoCount: snapshot.publicRepoCount,
    followersCount: snapshot.followersCount ?? 0,
    followingCount: snapshot.followingCount ?? 0,
    totalStars: snapshot.totalStars ?? 0,
    totalCommits: snapshot.totalCommits ?? 0,
    createdAt: snapshot.createdAt,
    contributionDays: (snapshot.contributionDays ?? []).map((day) => ({
      date: day.date,
      count: day.count,
      level: day.level,
    })),
  };
}

export function normalizeStatItem(item: StatItemApi): StatItem {
  return {
    id: item.id,
    label: item.label,
    value: item.value,
    description: item.description,
    actionLabel: item.actionLabel ?? undefined,
    meta: item.meta ?? undefined,
    footnote: item.footnote ?? undefined,
  };
}

export function normalizeStats(stats: StatsApi): StatsPageData {
  return {
    contributionWeeks: stats.contributionWeeks ?? [],
    githubSummary: normalizeStatItem(stats.githubSummary),
    latestGithubSnapshot: normalizeGithubSnapshot(stats.latestGithubSnapshot),
    portfolioHighlights: (stats.portfolioHighlights ?? []).map((item) => normalizeStatItem(item)),
    portfolioStats: (stats.portfolioStats ?? []).map((item) => normalizeStatItem(item)),
    monthLabels: stats.monthLabels ?? [],
    weekdayLabels: stats.weekdayLabels ?? [],
  };
}

function toHeroAction(
  label: string | null | undefined,
  url: string | null | undefined,
  appearance: 'primary' | 'secondary' | 'ghost'
): Profile['heroActions'][number] | null {
  if (!label || !url) {
    return null;
  }

  if (url.startsWith('/')) {
    return {
      label,
      appearance,
      routerLink: url,
      openInNewTab: false,
    };
  }

  return {
    label,
    appearance,
    href: url,
    openInNewTab: true,
  };
}

function formatDate(value: string | null | undefined): string {
  if (!value) {
    return '';
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

function formatPeriod(startDate: string, endDate?: string | null, isCurrent?: boolean): string {
  const start = formatMonthYear(startDate);
  const end = isCurrent ? 'Present' : endDate ? formatMonthYear(endDate) : 'Present';
  return `${start} - ${end}`;
}

function formatMonthYear(value: string): string {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return parsed.toLocaleDateString('en-GB', {
    month: 'short',
    year: 'numeric',
  });
}
