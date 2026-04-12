import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { API_BASE_URL } from '../../core/config/api.config';
import { BlogPost } from '../models/blog-post.model';
import { ContactMessageCreatedResponse, ContactMessageDraft } from '../models/contact-message.model';
import { ContactMethod } from '../models/contact-method.model';
import { Experience } from '../models/experience.model';
import { GithubSnapshot } from '../models/github-snapshot.model';
import { HomePageData } from '../models/home.model';
import { Profile } from '../models/profile.model';
import { Project, ProjectLink } from '../models/project.model';
import { ResolvedMedia } from '../models/resolved-media.model';
import { SiteShellData, NavigationItem } from '../models/site-shell.model';
import { SocialLink } from '../models/social-link.model';
import { StatItem } from '../models/stat-item.model';
import { StatsPageData } from '../models/stats-page.model';
import { SiteEventCreatePayload } from '../models/site-event.model';

interface CollectionResponse<T> {
  items?: T[] | null;
  total?: number;
}

interface MediaApi {
  id: string;
  url: string;
  alt?: string | null;
  fileName?: string | null;
  mimeType?: string | null;
  width?: number | null;
  height?: number | null;
}

interface SocialLinkApi {
  id: string;
  profileId: string;
  platform: string;
  label: string;
  url: string;
  iconKey?: string | null;
  sortOrder: number;
  isVisible: boolean;
}

interface NavigationItemApi {
  id: string;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

interface SkillApi {
  id: string;
  categoryId: string;
  name: string;
  yearsOfExperience?: number | null;
  iconKey?: string | null;
  sortOrder: number;
  isHighlighted: boolean;
}

interface ExpertiseGroupApi {
  title: string;
  tags: string[];
}

interface ProfileApi {
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

interface ProjectImageApi {
  id: string;
  projectId: string;
  imageFileId?: string | null;
  altText?: string | null;
  sortOrder: number;
  isCover: boolean;
  image?: MediaApi | null;
}

interface ProjectApi {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  summary?: string | null;
  descriptionMarkdown?: string | null;
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
  state: Project['state'];
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  createdAt: string;
  updatedAt: string;
  skills: SkillApi[];
  images: ProjectImageApi[];
}

interface BlogTagApi {
  id: string;
  name: string;
  slug: string;
}

interface BlogPostApi {
  id: string;
  slug: string;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId?: string | null;
  coverImageAlt?: string | null;
  coverImage?: MediaApi | null;
  readingTimeMinutes?: number | null;
  status: BlogPost['status'];
  isFeatured: boolean;
  publishedAt?: string | null;
  seoTitle?: string | null;
  seoDescription?: string | null;
  createdAt: string;
  updatedAt: string;
  tags: BlogTagApi[];
}

interface ExperienceApi {
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

interface ContactMethodApi {
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

interface SiteShellApi {
  navigation: CollectionResponse<NavigationItemApi>;
  profile: ProfileApi;
  footerText: string;
  contactMethods: ContactMethodApi[];
}

interface HomeApi {
  hero: ProfileApi;
  featuredProjects: ProjectApi[];
  featuredBlogPosts: BlogPostApi[];
  expertiseGroups: ExpertiseGroupApi[];
  experiencePreview: ExperienceApi[];
  contactPreview: ContactMethodApi[];
}

interface GithubContributionDayApi {
  date: string;
  count: number;
  level: number;
}

interface GithubSnapshotApi {
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

interface StatItemApi {
  id: string;
  label: string;
  value: string;
  description: string;
  actionLabel?: string | null;
  meta?: string | null;
  footnote?: string | null;
}

interface StatsApi {
  contributionWeeks: number[][];
  githubSummary: StatItemApi;
  latestGithubSnapshot: GithubSnapshotApi;
  portfolioHighlights: StatItemApi[];
  portfolioStats: StatItemApi[];
  monthLabels: string[];
  weekdayLabels: string[];
}

@Injectable({ providedIn: 'root' })
export class PublicPortfolioApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  getProfile(): Observable<Profile> {
    return this.http.get<ProfileApi>(`${this.apiBaseUrl}/public/profile`).pipe(map((profile) => this.normalizeProfile(profile)));
  }

  getNavigation(): Observable<NavigationItem[]> {
    return this.http
      .get<CollectionResponse<NavigationItemApi>>(`${this.apiBaseUrl}/public/navigation`)
      .pipe(map((response) => (response.items ?? []).map((item) => this.normalizeNavigationItem(item))));
  }

  getSiteShell(): Observable<SiteShellData> {
    return this.http.get<SiteShellApi>(`${this.apiBaseUrl}/public/site-shell`).pipe(
      map((shell) => ({
        navigation: (shell.navigation.items ?? []).map((item) => this.normalizeNavigationItem(item)),
        profile: this.normalizeProfile(shell.profile),
        footerText: shell.footerText ?? '',
        contactMethods: this.normalizeContactMethods(shell.contactMethods),
      }))
    );
  }

  getHome(): Observable<HomePageData> {
    return this.http.get<HomeApi>(`${this.apiBaseUrl}/public/home`).pipe(
      map((home) => ({
        hero: this.normalizeProfile(home.hero),
        featuredProjects: this.normalizeProjects(home.featuredProjects),
        featuredBlogPosts: this.normalizeBlogPosts(home.featuredBlogPosts),
        expertiseGroups: home.expertiseGroups ?? [],
        experiencePreview: this.normalizeExperienceList(home.experiencePreview),
        contactPreview: this.normalizeContactMethods(home.contactPreview),
      }))
    );
  }

  getProjects(): Observable<Project[]> {
    return this.http
      .get<CollectionResponse<ProjectApi>>(`${this.apiBaseUrl}/public/projects`)
      .pipe(map((response) => this.normalizeProjects(response.items)));
  }

  getProjectBySlug(slug: string): Observable<Project> {
    return this.http.get<ProjectApi>(`${this.apiBaseUrl}/public/projects/${slug}`).pipe(map((project) => this.normalizeProject(project)));
  }

  getBlogPosts(): Observable<BlogPost[]> {
    return this.http
      .get<CollectionResponse<BlogPostApi>>(`${this.apiBaseUrl}/public/blog-posts`)
      .pipe(map((response) => this.normalizeBlogPosts(response.items)));
  }

  getBlogPostBySlug(slug: string): Observable<BlogPost> {
    return this.http.get<BlogPostApi>(`${this.apiBaseUrl}/public/blog-posts/${slug}`).pipe(map((post) => this.normalizeBlogPost(post)));
  }

  getExperience(): Observable<Experience[]> {
    return this.http
      .get<CollectionResponse<ExperienceApi>>(`${this.apiBaseUrl}/public/experience`)
      .pipe(map((response) => this.normalizeExperienceList(response.items)));
  }

  getGithubSnapshot(): Observable<GithubSnapshot> {
    return this.http.get<GithubSnapshotApi>(`${this.apiBaseUrl}/public/github`).pipe(map((snapshot) => this.normalizeGithubSnapshot(snapshot)));
  }

  getStats(): Observable<StatsPageData> {
    return this.http.get<StatsApi>(`${this.apiBaseUrl}/public/stats`).pipe(map((stats) => this.normalizeStats(stats)));
  }

  submitContactMessage(payload: ContactMessageDraft): Observable<ContactMessageCreatedResponse> {
    return this.http.post<ContactMessageCreatedResponse>(`${this.apiBaseUrl}/contact/messages`, payload);
  }

  createSiteEvent(payload: SiteEventCreatePayload): Observable<{ message: string; eventId: string }> {
    return this.http.post<{ message: string; eventId: string }>(`${this.apiBaseUrl}/events`, payload);
  }

  private normalizeNavigationItem(item: NavigationItemApi): NavigationItem {
    return {
      id: item.id,
      label: item.label,
      routePath: item.routePath,
      isExternal: item.isExternal,
      sortOrder: item.sortOrder,
      isVisible: item.isVisible,
    };
  }

  private normalizeProfile(profile: ProfileApi): Profile {
    const fullName = [profile.firstName, profile.lastName].filter(Boolean).join(' ').trim();
    const longBio = profile.longBio ?? '';
    const shortIntro = profile.shortIntro ?? '';
    const headline = profile.headline ?? 'Portfolio Builder';
    const socialLinks = this.normalizeSocialLinks(profile.socialLinks);
    const heroActions = [
      this.toHeroAction(profile.ctaPrimaryLabel, profile.ctaPrimaryUrl, 'primary'),
      this.toHeroAction(profile.ctaSecondaryLabel, profile.ctaSecondaryUrl, 'secondary')
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
      avatarUrl: this.normalizeMedia(profile.avatar)?.url ?? '',
      heroImageUrl: this.normalizeMedia(profile.heroImage)?.url ?? '',
      resumeUrl: this.normalizeMedia(profile.resume)?.url ?? '',
      skills: Array.isArray(profile.skills) ? profile.skills : [],
      expertiseGroups: Array.isArray(profile.expertiseGroups) ? profile.expertiseGroups : [],
      introParagraphs: Array.isArray(profile.introParagraphs) ? profile.introParagraphs : [shortIntro, longBio].filter(Boolean),
      availability: Array.isArray(profile.availability) ? profile.availability : [],
      heroActions,
      socialLinks,
      createdAt: profile.createdAt,
      updatedAt: profile.updatedAt
    };
  }

  private normalizeMedia(media: MediaApi | null | undefined): ResolvedMedia | null {
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

  private normalizeSocialLinks(items: SocialLinkApi[] | null | undefined): SocialLink[] {
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
      isVisible: link.isVisible
    }));
  }

  private normalizeContactMethods(items: ContactMethodApi[] | null | undefined): ContactMethod[] {
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

  private toHeroAction(
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
        openInNewTab: false
      };
    }

    return {
      label,
      appearance,
      href: url,
      openInNewTab: true
    };
  }

  private normalizeProjects(items: ProjectApi[] | null | undefined): Project[] {
    if (!Array.isArray(items)) {
      return [];
    }

    return items.map((project) => this.normalizeProject(project));
  }

  private normalizeProject(project: ProjectApi): Project {
    const orderedSkills = [...(project.skills ?? [])].sort((left, right) => left.sortOrder - right.sortOrder || left.name.localeCompare(right.name));
    const orderedImages = [...(project.images ?? [])].sort((left, right) => left.sortOrder - right.sortOrder);
    const coverImage = this.normalizeMedia(project.coverImage) ?? this.normalizeMedia(orderedImages.find((image) => image.isCover)?.image) ?? this.normalizeMedia(orderedImages[0]?.image);
    const coverAlt = coverImage?.alt ?? orderedImages.find((image) => image.isCover)?.altText ?? orderedImages[0]?.altText ?? project.title;
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
      descriptionMarkdown: project.descriptionMarkdown ?? undefined,
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

  private normalizeBlogPosts(items: BlogPostApi[] | null | undefined): BlogPost[] {
    if (!Array.isArray(items)) {
      return [];
    }

    return items.map((post) => this.normalizeBlogPost(post));
  }

  private normalizeBlogPost(post: BlogPostApi): BlogPost {
    const tagNames = Array.isArray(post.tags) ? post.tags.map((tag) => tag.name) : [];
    const readingTimeMinutes = typeof post.readingTimeMinutes === 'number' ? post.readingTimeMinutes : 0;
    const cover = this.normalizeMedia(post.coverImage);
    const coverAlt = cover?.alt ?? post.coverImageAlt ?? 'Blog post cover placeholder';

    return {
      id: post.id,
      slug: post.slug,
      title: post.title,
      excerpt: post.excerpt ?? '',
      publishedAt: this.formatDate(post.publishedAt),
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
      contentMarkdown: post.contentMarkdown ?? '',
      seoTitle: post.seoTitle ?? undefined,
      seoDescription: post.seoDescription ?? undefined
    };
  }

  private normalizeExperienceList(items: ExperienceApi[] | null | undefined): Experience[] {
    if (!Array.isArray(items)) {
      return [];
    }

    return items.map((item) => this.normalizeExperience(item));
  }

  private normalizeExperience(item: ExperienceApi): Experience {
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
      period: this.formatPeriod(item.startDate, item.endDate, item.isCurrent),
      summary: item.summary,
      descriptionMarkdown: item.descriptionMarkdown ?? undefined,
      logoFileId: item.logoFileId ?? null,
      logoUrl: this.normalizeMedia(item.logo)?.url ?? undefined,
      sortOrder: item.sortOrder,
      skillNames: Array.isArray(item.skillNames) ? item.skillNames : [],
    };
  }

  private normalizeGithubSnapshot(snapshot: GithubSnapshotApi): GithubSnapshot {
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

  private normalizeStatItem(item: StatItemApi): StatItem {
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

  private normalizeStats(stats: StatsApi): StatsPageData {
    return {
      contributionWeeks: stats.contributionWeeks ?? [],
      githubSummary: this.normalizeStatItem(stats.githubSummary),
      latestGithubSnapshot: this.normalizeGithubSnapshot(stats.latestGithubSnapshot),
      portfolioHighlights: (stats.portfolioHighlights ?? []).map((item) => this.normalizeStatItem(item)),
      portfolioStats: (stats.portfolioStats ?? []).map((item) => this.normalizeStatItem(item)),
      monthLabels: stats.monthLabels ?? [],
      weekdayLabels: stats.weekdayLabels ?? [],
    };
  }

  private formatDate(value: string | null | undefined): string {
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
      year: 'numeric'
    });
  }

  private formatPeriod(startDate: string, endDate?: string | null, isCurrent?: boolean): string {
    const start = this.formatMonthYear(startDate);
    const end = isCurrent ? 'Present' : endDate ? this.formatMonthYear(endDate) : 'Present';
    return `${start} - ${end}`;
  }

  private formatMonthYear(value: string): string {
    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) {
      return value;
    }

    return parsed.toLocaleDateString('en-GB', {
      month: 'short',
      year: 'numeric'
    });
  }
}
