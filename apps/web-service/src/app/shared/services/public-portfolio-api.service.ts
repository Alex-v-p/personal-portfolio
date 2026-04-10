import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { API_BASE_URL } from '../../core/config/api.config';
import { BlogPost } from '../models/blog-post.model';
import { ContactMessageCreatedResponse, ContactMessageDraft } from '../models/contact-message.model';
import { Profile } from '../models/profile.model';
import { Project, ProjectLink } from '../models/project.model';
import { SocialLink } from '../models/social-link.model';

interface CollectionResponse<T> {
  items?: T[] | null;
  total?: number;
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
  ctaPrimaryLabel?: string | null;
  ctaPrimaryUrl?: string | null;
  ctaSecondaryLabel?: string | null;
  ctaSecondaryUrl?: string | null;
  isPublic: boolean;
  socialLinks: SocialLinkApi[];
  createdAt: string;
  updatedAt: string;
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

interface ProjectImageApi {
  id: string;
  projectId: string;
  imageFileId?: string | null;
  altText?: string | null;
  sortOrder: number;
  isCover: boolean;
}

interface ProjectApi {
  id: string;
  slug: string;
  title: string;
  teaser: string;
  summary?: string | null;
  descriptionMarkdown?: string | null;
  coverImageFileId?: string | null;
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

@Injectable({ providedIn: 'root' })
export class PublicPortfolioApiService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = inject(API_BASE_URL);

  getProfile(): Observable<Profile> {
    return this.http.get<ProfileApi>(`${this.apiBaseUrl}/public/profile`).pipe(map((profile) => this.normalizeProfile(profile)));
  }

  getProjects(): Observable<Project[]> {
    return this.http
      .get<CollectionResponse<ProjectApi>>(`${this.apiBaseUrl}/public/projects`)
      .pipe(map((response) => this.normalizeProjects(response.items)));
  }

  getBlogPosts(): Observable<BlogPost[]> {
    return this.http
      .get<CollectionResponse<BlogPostApi>>(`${this.apiBaseUrl}/public/blog-posts`)
      .pipe(map((response) => this.normalizeBlogPosts(response.items)));
  }

  getBlogPostBySlug(slug: string): Observable<BlogPost> {
    return this.http.get<BlogPostApi>(`${this.apiBaseUrl}/public/blog-posts/${slug}`).pipe(map((post) => this.normalizeBlogPost(post)));
  }

  submitContactMessage(payload: ContactMessageDraft): Observable<ContactMessageCreatedResponse> {
    return this.http.post<ContactMessageCreatedResponse>(`${this.apiBaseUrl}/contact/messages`, payload);
  }

  private normalizeProfile(profile: ProfileApi): Profile {
    const fullName = [profile.firstName, profile.lastName].filter(Boolean).join(' ').trim();
    const longBio = profile.longBio ?? '';
    const shortIntro = profile.shortIntro ?? '';
    const headline = profile.headline ?? 'Portfolio Builder';
    const socialLinks = this.normalizeSocialLinks(profile.socialLinks);
    const heroActions = [
      this.toHeroAction(profile.ctaPrimaryLabel, profile.ctaPrimaryUrl, 'secondary'),
      this.toHeroAction(profile.ctaSecondaryLabel, profile.ctaSecondaryUrl, 'primary')
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
      footerDescription: longBio || shortIntro,
      avatarFileId: profile.avatarFileId ?? null,
      heroImageFileId: profile.heroImageFileId ?? null,
      resumeFileId: profile.resumeFileId ?? null,
      skills: [],
      expertiseGroups: [],
      introParagraphs: [shortIntro, longBio].filter((value): value is string => !!value),
      availability: [],
      heroActions,
      socialLinks,
      createdAt: profile.createdAt,
      updatedAt: profile.updatedAt
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
    const coverImage = orderedImages.find((image) => image.isCover) ?? orderedImages[0];
    const tags = orderedSkills.map((skill) => skill.name);
    const links: ProjectLink[] = [];

    if (project.githubUrl) {
      links.push({ label: 'GitHub', href: project.githubUrl });
    }

    if (project.demoUrl) {
      links.unshift({ label: 'Live Demo', href: project.demoUrl });
    }

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
      imageAlt: coverImage?.altText ?? project.title,
      coverImageAlt: coverImage?.altText ?? project.title,
      coverImageFileId: project.coverImageFileId ?? coverImage?.imageFileId ?? null,
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
      coverAlt: post.coverImageAlt ?? 'Blog post cover placeholder',
      coverImageAlt: post.coverImageAlt ?? 'Blog post cover placeholder',
      coverImageFileId: post.coverImageFileId ?? null,
      status: post.status,
      contentMarkdown: post.contentMarkdown ?? '',
      seoTitle: post.seoTitle ?? undefined,
      seoDescription: post.seoDescription ?? undefined
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
}
