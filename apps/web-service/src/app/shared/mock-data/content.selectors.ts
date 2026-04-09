import { BlogPostTag } from '../models/blog-post-tag.model';
import { BlogPost } from '../models/blog-post.model';
import { ContactMethod } from '../models/contact-method.model';
import { Experience } from '../models/experience.model';
import { NavigationItem } from '../models/navigation-item.model';
import { Profile } from '../models/profile.model';
import { Project } from '../models/project.model';
import { SkillCategory } from '../models/skill-category.model';
import { Skill } from '../models/skill.model';
import { SocialLink } from '../models/social-link.model';
import { MediaFile } from '../models/media-file.model';
import { GithubContributionDay } from '../models/github-contribution-day.model';
import { GithubSnapshot } from '../models/github-snapshot.model';
import { StatItem } from '../models/stat-item.model';
import { BlogTag } from '../models/blog-tag.model';

export interface ProfileRecord {
  id: string;
  firstName: string;
  lastName: string;
  headline: string;
  shortIntro: string;
  longBio: string;
  location: string;
  email: string;
  phone: string;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  ctaPrimaryLabel: string;
  ctaPrimaryUrl: string;
  ctaSecondaryLabel: string;
  ctaSecondaryUrl: string;
  createdAt: string;
  updatedAt: string;
}

export interface ExperienceRecord {
  id: string;
  organizationName: string;
  roleTitle: string;
  location: string;
  experienceType: string;
  startDate: string;
  endDate?: string | null;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown?: string;
  logoFileId?: string | null;
  sortOrder: number;
}

export interface ProjectRecord {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  summary: string;
  descriptionMarkdown?: string;
  coverImageFileId?: string | null;
  githubUrl?: string;
  githubRepoName?: string;
  demoUrl?: string;
  startedOn?: string | null;
  endedOn?: string | null;
  durationLabel: string;
  isFeatured: boolean;
  sortOrder: number;
  publishedAt?: string | null;
  state: 'published' | 'archived' | 'completed' | 'paused';
  organizationName: string;
  highlight: string;
}

export interface BlogPostRecord {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId?: string | null;
  coverImageAlt?: string;
  readingTimeMinutes: number;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt: string;
  seoTitle?: string;
  seoDescription?: string;
  category: string;
}

const formatDateRange = (startDate: string, endDate?: string | null, isCurrent = false): string => {
  const start = new Date(startDate).toLocaleDateString('en-GB', { month: 'short', year: 'numeric' });

  if (isCurrent) {
    return `${start} - present`;
  }

  if (!endDate) {
    return start;
  }

  const end = new Date(endDate).toLocaleDateString('en-GB', { month: 'short', year: 'numeric' });
  return `${start} - ${end}`;
};

const humanizeProjectState = (state: Project['state']): string => {
  const labels: Record<Project['state'], string> = {
    published: 'Published',
    archived: 'Archived',
    completed: 'Completed',
    paused: 'Paused'
  };

  return labels[state];
};

const getFile = (files: MediaFile[], fileId?: string | null): MediaFile | undefined => files.find((file) => file.id === fileId);

const getSkillNameMap = (skills: Skill[]): Map<string, Skill> => new Map(skills.map((skill) => [skill.id, skill]));

const resolveSkillNames = (skillIds: string[], skills: Skill[]): string[] => {
  const map = getSkillNameMap(skills);
  return skillIds
    .map((skillId) => map.get(skillId)?.name)
    .filter((name): name is string => Boolean(name));
};

const toExternalAction = (label: string, url: string, appearance: 'primary' | 'secondary' | 'ghost') => {
  const isInternal = url.startsWith('/');

  return isInternal
    ? { label, appearance, routerLink: url }
    : { label, appearance, href: url, openInNewTab: true };
};

export const buildProfileView = (
  profile: ProfileRecord,
  files: MediaFile[],
  categories: SkillCategory[],
  skills: Skill[]
): Profile => {
  const highlightedSkills = skills.filter((skill) => skill.isHighlighted).map((skill) => skill.name);
  const expertiseGroups = categories.map((category) => ({
    title: category.name,
    tags: skills
      .filter((skill) => skill.categoryId === category.id)
      .sort((a, b) => a.sortOrder - b.sortOrder)
      .map((skill) => skill.name)
  }));

  const fullName = `${profile.firstName} ${profile.lastName}`;
  const avatarFile = getFile(files, profile.avatarFileId);
  const heroFile = getFile(files, profile.heroImageFileId);
  const resumeFile = getFile(files, profile.resumeFileId);

  return {
    id: profile.id,
    firstName: profile.firstName,
    lastName: profile.lastName,
    name: fullName,
    headline: profile.headline,
    role: profile.headline,
    greeting: `Hi, I'm ${profile.firstName}`,
    location: profile.location,
    email: profile.email,
    phone: profile.phone,
    shortIntro: profile.shortIntro,
    longBio: profile.longBio,
    heroTitle: `I’m ${profile.headline}`,
    summary: profile.shortIntro,
    shortBio: 'I build portfolio sites, data-heavy student projects, and full-stack applications with a focus on maintainable architecture, thoughtful UI, and future-friendly structure.',
    footerDescription: 'Applied Computer Science student focused on AI, web development, and building practical digital products that are easy to maintain.',
    avatarFileId: profile.avatarFileId,
    heroImageFileId: profile.heroImageFileId,
    resumeFileId: profile.resumeFileId,
    avatarUrl: avatarFile?.publicUrl,
    heroImageUrl: heroFile?.publicUrl,
    resumeUrl: resumeFile?.publicUrl,
    skills: highlightedSkills,
    expertiseGroups,
    introParagraphs: [
      'I like building systems that feel simple on the surface and are well-structured underneath. That includes thoughtful UI, clean component design, and backend work that supports growth later.',
      'This mock portfolio content is intentionally organised around entity-shaped data, so a future API can return relational content without forcing a front-end rewrite.'
    ],
    availability: ['Open to internships', 'Open to freelance', 'Based in Belgium'],
    heroActions: [
      toExternalAction(profile.ctaPrimaryLabel, profile.ctaPrimaryUrl, 'secondary'),
      toExternalAction(profile.ctaSecondaryLabel, profile.ctaSecondaryUrl, 'primary')
    ],
    createdAt: profile.createdAt,
    updatedAt: profile.updatedAt
  };
};

export const buildExperienceViews = (
  records: ExperienceRecord[],
  files: MediaFile[]
): Experience[] => records
  .slice()
  .sort((a, b) => a.sortOrder - b.sortOrder)
  .map((record) => ({
    id: record.id,
    organizationName: record.organizationName,
    roleTitle: record.roleTitle,
    title: record.roleTitle,
    organization: record.organizationName,
    location: record.location,
    experienceType: record.experienceType,
    startDate: record.startDate,
    endDate: record.endDate,
    isCurrent: record.isCurrent,
    period: formatDateRange(record.startDate, record.endDate, record.isCurrent),
    summary: record.summary,
    descriptionMarkdown: record.descriptionMarkdown,
    logoFileId: record.logoFileId,
    logoUrl: getFile(files, record.logoFileId)?.publicUrl,
    sortOrder: record.sortOrder
  }));

export const buildProjectViews = (
  records: ProjectRecord[],
  files: MediaFile[],
  skills: Skill[],
  categories: SkillCategory[],
  projectSkills: { projectId: string; skillId: string }[]
): Project[] => records
  .slice()
  .sort((a, b) => a.sortOrder - b.sortOrder)
  .map((record) => {
    const skillIds = projectSkills.filter((entry) => entry.projectId === record.id).map((entry) => entry.skillId);
    const tagNames = resolveSkillNames(skillIds, skills);
    const skillMap = getSkillNameMap(skills);
    const primarySkill = skillIds.map((skillId) => skillMap.get(skillId)).find((skill): skill is Skill => Boolean(skill));
    const categoryName = categories.find((category) => category.id === primarySkill?.categoryId)?.name ?? 'Project';
    const cover = getFile(files, record.coverImageFileId);

    return {
      id: record.id,
      slug: record.slug,
      title: record.title,
      teaser: record.teaser,
      shortDescription: record.teaser,
      summary: record.summary,
      descriptionMarkdown: record.descriptionMarkdown,
      organization: record.organizationName,
      duration: record.durationLabel,
      durationLabel: record.durationLabel,
      status: humanizeProjectState(record.state),
      state: record.state,
      category: categoryName,
      tags: tagNames,
      featured: record.isFeatured,
      isFeatured: record.isFeatured,
      imageAlt: cover?.altText ?? 'Project image',
      coverImageAlt: cover?.altText ?? 'Project image',
      coverImageFileId: record.coverImageFileId,
      coverImageUrl: cover?.publicUrl,
      highlight: record.highlight,
      githubUrl: record.githubUrl,
      githubRepoName: record.githubRepoName,
      demoUrl: record.demoUrl,
      startedOn: record.startedOn,
      endedOn: record.endedOn,
      publishedAt: record.publishedAt,
      sortOrder: record.sortOrder,
      links: [
        { label: 'Read More', routerLink: ['/projects'] },
        ...(record.githubUrl ? [{ label: 'GitHub README', href: record.githubUrl }] : []),
        ...(record.demoUrl ? [{ label: 'Live Demo', href: record.demoUrl }] : [])
      ]
    };
  });

export const buildBlogPostViews = (
  records: BlogPostRecord[],
  files: MediaFile[],
  tags: BlogTag[],
  relations: BlogPostTag[]
): BlogPost[] => records.map((record) => {
  const cover = getFile(files, record.coverImageFileId);
  const tagNameMap = new Map(tags.map((tag) => [tag.id, tag.name]));
  const tagNames = relations
    .filter((relation) => relation.postId === record.id)
    .map((relation) => tagNameMap.get(relation.tagId))
    .filter((name): name is string => Boolean(name));

  return {
    id: record.id,
    slug: record.slug,
    title: record.title,
    excerpt: record.excerpt,
    publishedAt: record.publishedAt,
    readTime: `${record.readingTimeMinutes} min read`,
    readingTimeMinutes: record.readingTimeMinutes,
    category: record.category,
    tags: tagNames,
    featured: record.isFeatured,
    isFeatured: record.isFeatured,
    coverAlt: record.coverImageAlt ?? cover?.altText ?? 'Blog post cover',
    coverImageAlt: record.coverImageAlt ?? cover?.altText ?? 'Blog post cover',
    coverImageFileId: record.coverImageFileId,
    coverImageUrl: cover?.publicUrl,
    status: record.status,
    contentMarkdown: record.contentMarkdown,
    seoTitle: record.seoTitle,
    seoDescription: record.seoDescription
  };
});

export const buildContactMethods = (profile: Profile, socialLinks: SocialLink[]): ContactMethod[] => {
  const methods: ContactMethod[] = [
    {
      id: 'contact-email',
      platform: 'email',
      label: 'Email',
      value: profile.email,
      href: `mailto:${profile.email}`,
      actionLabel: 'Send Email',
      iconKey: 'mail',
      description: 'Best for project enquiries, internships, and collaboration.',
      sortOrder: 1,
      isVisible: true
    },
    {
      id: 'contact-phone',
      platform: 'phone',
      label: 'Phone',
      value: profile.phone,
      href: `tel:${profile.phone.replace(/\s+/g, '')}`,
      actionLabel: 'Call',
      iconKey: 'phone',
      description: 'Useful for quick coordination or planning a meeting.',
      sortOrder: 2,
      isVisible: true
    },
    ...socialLinks.map((link) => ({
      id: `contact-${link.platform}`,
      platform: link.platform,
      label: link.label,
      value: link.url.replace(/^https?:\/\//, ''),
      href: link.url,
      actionLabel: link.platform === 'github' || link.platform === 'linkedin' ? 'Connect +' : 'Open',
      iconKey: link.iconKey,
      description:
        link.platform === 'github'
          ? 'Code samples, experiments, and longer-form project work.'
          : link.platform === 'linkedin'
            ? 'Professional background, study path, and experience.'
            : 'Direct line for portfolio contact.',
      sortOrder: link.sortOrder + 2,
      isVisible: link.isVisible
    })),
    {
      id: 'contact-location',
      platform: 'location',
      label: 'Location',
      value: profile.location,
      href: `https://maps.google.com/?q=${encodeURIComponent(profile.location)}`,
      actionLabel: 'View Map',
      iconKey: 'map-pin',
      description: 'Available for on-site, hybrid, or remote collaboration.',
      sortOrder: 99,
      isVisible: true
    }
  ];

  return methods
    .filter((method) => method.isVisible)
    .sort((a, b) => a.sortOrder - b.sortOrder);
};

export const buildVisibleNavigation = (items: NavigationItem[]): NavigationItem[] => items
  .filter((item) => item.isVisible)
  .sort((a, b) => a.sortOrder - b.sortOrder);

export const buildGithubSummary = (snapshot: GithubSnapshot): StatItem => ({
  id: 'public-repos',
  label: 'Public Repo’s',
  value: String(snapshot.publicRepoCount),
  description: 'Latest mocked snapshot based on the future github_snapshots table.',
  meta: `${snapshot.username} · ${snapshot.snapshotDate}`
});

export const buildPortfolioStats = (
  projects: Project[],
  posts: BlogPost[],
  skills: Skill[],
  snapshot: GithubSnapshot
): StatItem[] => [
  {
    id: 'project-count',
    label: 'Total Projects',
    value: String(projects.length),
    description: 'Portfolio projects currently available in the relational mock dataset.'
  },
  {
    id: 'blog-count',
    label: 'Blog Posts',
    value: String(posts.filter((post) => post.status === 'published').length),
    description: 'Published mock articles available for the blog listing.'
  },
  {
    id: 'tech-count',
    label: 'Tech Count',
    value: String(new Set(skills.map((skill) => skill.name)).size),
    description: 'Unique skills referenced by the portfolio content and lookup tables.',
    actionLabel: 'Love this portfolio'
  },
  {
    id: 'total-stars',
    label: 'GitHub Stars',
    value: String(snapshot.totalStars),
    description: 'Mocked aggregate stars stored in the github_snapshots table.'
  }
];

export const buildContributionCells = (days: GithubContributionDay[], snapshotId: string): number[] => days
  .filter((day) => day.snapshotId === snapshotId)
  .map((day) => day.level);

export const buildContributionWeeks = (days: GithubContributionDay[], snapshotId: string): number[][] => {
  const cells = buildContributionCells(days, snapshotId);
  const weeks: number[][] = [];

  for (let index = 0; index < cells.length; index += 7) {
    const week = cells.slice(index, index + 7);

    while (week.length < 7) {
      week.push(0);
    }

    weeks.push(week);
  }

  return weeks;
};
