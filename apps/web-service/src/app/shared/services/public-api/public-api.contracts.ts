import { BlogPostStatus } from '../../models/blog-post-summary.model';
import { ProjectState } from '../../models/project-summary.model';

export interface CollectionResponse<T> {
  items?: T[] | null;
  total?: number;
}

export interface MediaApi {
  id: string;
  url: string;
  alt?: string | null;
  fileName?: string | null;
  mimeType?: string | null;
  width?: number | null;
  height?: number | null;
}

export interface SocialLinkApi {
  id: string;
  profileId: string;
  platform: string;
  label: string;
  url: string;
  iconKey?: string | null;
  sortOrder: number;
  isVisible: boolean;
}

export interface NavigationItemApi {
  id: string;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface SkillApi {
  id: string;
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface ExpertiseGroupApi {
  title: string;
  tags: string[];
}

export interface ProfileApi {
  id: string;
  firstName: string;
  lastName: string;
  headline: string;
  shortIntro: string;
  longBio?: string | null;
  location?: string | null;
  email?: string | null;
  phone?: string | null;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  avatar?: MediaApi | null;
  heroImage?: MediaApi | null;
  resume?: MediaApi | null;
  ctaPrimaryLabel?: string | null;
  ctaPrimaryUrl?: string | null;
  ctaSecondaryLabel?: string | null;
  ctaSecondaryUrl?: string | null;
  isPublic: boolean;
  socialLinks: SocialLinkApi[];
  footerDescription: string;
  introParagraphs: string[];
  availability: string[];
  skills: string[];
  expertiseGroups: ExpertiseGroupApi[];
  createdAt: string;
  updatedAt: string;
}

export interface ProjectImageApi {
  id: string;
  projectId: string;
  imageFileId?: string | null;
  altText?: string | null;
  sortOrder: number;
  isCover: boolean;
  image?: MediaApi | null;
}

export interface ProjectSummaryApi {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  summary?: string | null;
  coverImageFileId?: string | null;
  coverImage?: MediaApi | null;
  githubUrl?: string | null;
  githubRepoOwner?: string | null;
  githubRepoName?: string | null;
  demoUrl?: string | null;
  companyName?: string | null;
  startedOn?: string | null;
  endedOn?: string | null;
  durationLabel: string;
  status: string;
  state: ProjectState;
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  createdAt: string;
  updatedAt: string;
  skills: SkillApi[];
}

export interface ProjectDetailApi extends ProjectSummaryApi {
  descriptionMarkdown?: string | null;
  images: ProjectImageApi[];
}

export interface BlogTagApi {
  id: string;
  name: string;
  slug: string;
}

export interface BlogPostSummaryApi {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  coverImage?: MediaApi | null;
  readingTimeMinutes?: number | null;
  status: BlogPostStatus;
  isFeatured: boolean;
  publishedAt?: string | null;
  createdAt: string;
  updatedAt: string;
  tags: BlogTagApi[];
}

export interface BlogPostDetailApi extends BlogPostSummaryApi {
  contentMarkdown: string;
  seoTitle?: string | null;
  seoDescription?: string | null;
}

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

export interface ContactMethodApi {
  id: string;
  platform: string;
  label: string;
  value: string;
  href: string;
  actionLabel: string;
  iconKey?: string | null;
  description?: string | null;
  sortOrder: number;
  isVisible: boolean;
}

export interface SiteShellApi {
  navigation: CollectionResponse<NavigationItemApi>;
  profile: ProfileApi;
  footerText: string;
  contactMethods: ContactMethodApi[];
}

export interface HomeApi {
  hero: ProfileApi;
  featuredProjects: ProjectSummaryApi[];
  featuredBlogPosts: BlogPostSummaryApi[];
  expertiseGroups: ExpertiseGroupApi[];
  experiencePreview: ExperienceApi[];
  contactPreview: ContactMethodApi[];
}

export interface GithubContributionDayApi {
  date: string;
  count: number;
  level: number;
}

export interface GithubSnapshotApi {
  id: string;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount?: number | null;
  followingCount?: number | null;
  totalStars?: number | null;
  totalCommits?: number | null;
  createdAt: string;
  contributionDays: GithubContributionDayApi[];
}

export interface StatItemApi {
  id: string;
  label: string;
  value: string;
  description: string;
  actionLabel?: string | null;
  meta?: string | null;
  footnote?: string | null;
}

export interface StatsApi {
  contributionWeeks: number[][];
  githubSummary: StatItemApi;
  latestGithubSnapshot: GithubSnapshotApi;
  portfolioHighlights: StatItemApi[];
  portfolioStats: StatItemApi[];
  monthLabels: string[];
  weekdayLabels: string[];
}
