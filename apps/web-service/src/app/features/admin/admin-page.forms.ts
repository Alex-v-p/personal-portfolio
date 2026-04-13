import {
  AdminBlogPost,
  AdminBlogTag,
  AdminExperience,
  AdminGithubSnapshot,
  AdminNavigationItem,
  AdminProfile,
  AdminProject,
  AdminSkillCategory,
  AdminSkillOption,
  AdminSocialLink,
  AdminUser,
} from '../../shared/models/admin.model';

export interface ScopedUploadForm {
  title: string;
  altText: string;
  description: string;
  visibility: 'public' | 'private' | 'signed';
  file: File | null;
}

export interface AdminProjectForm {
  id?: string | null;
  slug: string;
  title: string;
  teaser: string;
  summary: string;
  descriptionMarkdown: string;
  coverImageFileId: string | null;
  githubUrl: string;
  githubRepoOwner: string;
  githubRepoName: string;
  demoUrl: string;
  companyName: string;
  startedOn: string;
  endedOn: string;
  durationLabel: string;
  status: string;
  state: 'published' | 'archived' | 'completed' | 'paused';
  isFeatured: boolean;
  sortOrder: number;
  publishedAt: string;
  skillIds: string[];
}

export interface AdminBlogPostForm {
  id?: string | null;
  slug: string;
  title: string;
  excerpt: string;
  contentMarkdown: string;
  coverImageFileId: string | null;
  coverImageAlt: string;
  readingTimeMinutes: number | null;
  status: 'draft' | 'published' | 'archived';
  isFeatured: boolean;
  publishedAt: string;
  seoTitle: string;
  seoDescription: string;
  tagIds: string[];
}

export interface AdminProfileForm {
  id?: string;
  firstName: string;
  lastName: string;
  headline: string;
  shortIntro: string;
  longBio: string;
  location: string;
  email: string;
  phone: string;
  avatarFileId: string | null;
  heroImageFileId: string | null;
  resumeFileId: string | null;
  ctaPrimaryLabel: string;
  ctaPrimaryUrl: string;
  ctaSecondaryLabel: string;
  ctaSecondaryUrl: string;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
}

export interface AdminSkillCategoryForm {
  id?: string | null;
  name: string;
  description: string;
  sortOrder: number;
}

export interface AdminSkillForm {
  id?: string | null;
  categoryId: string;
  name: string;
  yearsOfExperience: number | null;
  iconKey: string;
  sortOrder: number;
  isHighlighted: boolean;
}

export interface AdminBlogTagForm {
  id?: string | null;
  name: string;
  slug: string;
}

export interface AdminExperienceForm {
  id?: string | null;
  organizationName: string;
  roleTitle: string;
  location: string;
  experienceType: string;
  startDate: string;
  endDate: string;
  isCurrent: boolean;
  summary: string;
  descriptionMarkdown: string;
  logoFileId: string | null;
  sortOrder: number;
  skillIds: string[];
}

export interface AdminNavigationItemForm {
  id?: string | null;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminUserForm {
  id?: string | null;
  email: string;
  displayName: string;
  password: string;
  isActive: boolean;
}

export interface AdminGithubSnapshotForm {
  id?: string | null;
  snapshotDate: string;
  username: string;
  publicRepoCount: number;
  followersCount: number | null;
  followingCount: number | null;
  totalStars: number | null;
  totalCommits: number | null;
  rawPayloadText: string;
  contributionDaysText: string;
}

export function createEmptyScopedUploadForm(): ScopedUploadForm {
  return { title: '', altText: '', description: '', visibility: 'public', file: null };
}

export function createEmptyProjectForm(): AdminProjectForm {
  return {
    slug: '',
    title: '',
    teaser: '',
    summary: '',
    descriptionMarkdown: '',
    coverImageFileId: null,
    githubUrl: '',
    githubRepoOwner: '',
    githubRepoName: '',
    demoUrl: '',
    companyName: '',
    startedOn: '',
    endedOn: '',
    durationLabel: '',
    status: '',
    state: 'published',
    isFeatured: false,
    sortOrder: 0,
    publishedAt: '',
    skillIds: []
  };
}

export function createEmptyBlogPostForm(): AdminBlogPostForm {
  return {
    slug: '',
    title: '',
    excerpt: '',
    contentMarkdown: '',
    coverImageFileId: null,
    coverImageAlt: '',
    readingTimeMinutes: null,
    status: 'draft',
    isFeatured: false,
    publishedAt: '',
    seoTitle: '',
    seoDescription: '',
    tagIds: []
  };
}

export function createEmptyProfileForm(): AdminProfileForm {
  return {
    firstName: '',
    lastName: '',
    headline: '',
    shortIntro: '',
    longBio: '',
    location: '',
    email: '',
    phone: '',
    avatarFileId: null,
    heroImageFileId: null,
    resumeFileId: null,
    ctaPrimaryLabel: '',
    ctaPrimaryUrl: '',
    ctaSecondaryLabel: '',
    ctaSecondaryUrl: '',
    isPublic: true,
    socialLinks: []
  };
}

export function createEmptySkillCategoryForm(): AdminSkillCategoryForm {
  return { name: '', description: '', sortOrder: 0 };
}

export function createEmptySkillForm(): AdminSkillForm {
  return { categoryId: '', name: '', yearsOfExperience: null, iconKey: '', sortOrder: 0, isHighlighted: false };
}

export function createEmptyBlogTagForm(): AdminBlogTagForm {
  return { name: '', slug: '' };
}

export function createEmptyExperienceForm(): AdminExperienceForm {
  return {
    organizationName: '',
    roleTitle: '',
    location: '',
    experienceType: 'work',
    startDate: '',
    endDate: '',
    isCurrent: false,
    summary: '',
    descriptionMarkdown: '',
    logoFileId: null,
    sortOrder: 0,
    skillIds: []
  };
}

export function createEmptyNavigationItemForm(): AdminNavigationItemForm {
  return { label: '', routePath: '', isExternal: false, sortOrder: 0, isVisible: true };
}

export function createEmptyAdminUserForm(): AdminUserForm {
  return { email: '', displayName: '', password: '', isActive: true };
}

export function createEmptyGithubSnapshotForm(): AdminGithubSnapshotForm {
  return {
    snapshotDate: '',
    username: 'Alex-v-p',
    publicRepoCount: 0,
    followersCount: null,
    followingCount: null,
    totalStars: null,
    totalCommits: null,
    rawPayloadText: '',
    contributionDaysText: '[]'
  };
}

export function toProjectForm(project: AdminProject): AdminProjectForm {
  return {
    id: project.id,
    slug: project.slug,
    title: project.title,
    teaser: project.teaser,
    summary: project.summary ?? '',
    descriptionMarkdown: project.descriptionMarkdown ?? '',
    coverImageFileId: project.coverImageFileId ?? null,
    githubUrl: project.githubUrl ?? '',
    githubRepoOwner: project.githubRepoOwner ?? '',
    githubRepoName: project.githubRepoName ?? '',
    demoUrl: project.demoUrl ?? '',
    companyName: project.companyName ?? '',
    startedOn: project.startedOn ?? '',
    endedOn: project.endedOn ?? '',
    durationLabel: project.durationLabel,
    status: project.status,
    state: project.state,
    isFeatured: project.isFeatured,
    sortOrder: project.sortOrder,
    publishedAt: project.publishedAt?.slice(0, 16) ?? '',
    skillIds: [...project.skillIds],
  };
}

export function toBlogPostForm(post: AdminBlogPost): AdminBlogPostForm {
  return {
    id: post.id,
    slug: post.slug,
    title: post.title,
    excerpt: post.excerpt,
    contentMarkdown: post.contentMarkdown,
    coverImageFileId: post.coverImageFileId ?? null,
    coverImageAlt: post.coverImageAlt ?? '',
    readingTimeMinutes: post.readingTimeMinutes ?? null,
    status: post.status,
    isFeatured: post.isFeatured,
    publishedAt: post.publishedAt?.slice(0, 16) ?? '',
    seoTitle: post.seoTitle ?? '',
    seoDescription: post.seoDescription ?? '',
    tagIds: [...post.tagIds],
  };
}

export function toProfileForm(profile: AdminProfile): AdminProfileForm {
  return {
    id: profile.id,
    firstName: profile.firstName,
    lastName: profile.lastName,
    headline: profile.headline,
    shortIntro: profile.shortIntro,
    longBio: profile.longBio ?? '',
    location: profile.location ?? '',
    email: profile.email ?? '',
    phone: profile.phone ?? '',
    avatarFileId: profile.avatarFileId ?? null,
    heroImageFileId: profile.heroImageFileId ?? null,
    resumeFileId: profile.resumeFileId ?? null,
    ctaPrimaryLabel: profile.ctaPrimaryLabel ?? '',
    ctaPrimaryUrl: profile.ctaPrimaryUrl ?? '',
    ctaSecondaryLabel: profile.ctaSecondaryLabel ?? '',
    ctaSecondaryUrl: profile.ctaSecondaryUrl ?? '',
    isPublic: profile.isPublic,
    socialLinks: profile.socialLinks.map((link) => ({ ...link })),
  };
}

export function toSkillCategoryForm(category: AdminSkillCategory): AdminSkillCategoryForm {
  return { id: category.id, name: category.name, description: category.description ?? '', sortOrder: category.sortOrder };
}

export function toSkillForm(skill: AdminSkillOption): AdminSkillForm {
  return {
    id: skill.id,
    categoryId: skill.categoryId,
    name: skill.name,
    yearsOfExperience: skill.yearsOfExperience ?? null,
    iconKey: skill.iconKey ?? '',
    sortOrder: skill.sortOrder,
    isHighlighted: skill.isHighlighted,
  };
}

export function toBlogTagForm(tag: AdminBlogTag): AdminBlogTagForm {
  return { id: tag.id, name: tag.name, slug: tag.slug };
}

export function toExperienceForm(experience: AdminExperience): AdminExperienceForm {
  return {
    id: experience.id,
    organizationName: experience.organizationName,
    roleTitle: experience.roleTitle,
    location: experience.location ?? '',
    experienceType: experience.experienceType,
    startDate: experience.startDate,
    endDate: experience.endDate ?? '',
    isCurrent: experience.isCurrent,
    summary: experience.summary,
    descriptionMarkdown: experience.descriptionMarkdown ?? '',
    logoFileId: experience.logoFileId ?? null,
    sortOrder: experience.sortOrder,
    skillIds: [...experience.skillIds],
  };
}

export function toNavigationItemForm(item: AdminNavigationItem): AdminNavigationItemForm {
  return {
    id: item.id,
    label: item.label,
    routePath: item.routePath,
    isExternal: item.isExternal,
    sortOrder: item.sortOrder,
    isVisible: item.isVisible,
  };
}

export function toAdminUserForm(user: AdminUser): AdminUserForm {
  return { id: user.id, email: user.email, displayName: user.displayName, password: '', isActive: user.isActive };
}

export function toGithubSnapshotForm(snapshot: AdminGithubSnapshot): AdminGithubSnapshotForm {
  return {
    id: snapshot.id,
    snapshotDate: snapshot.snapshotDate,
    username: snapshot.username,
    publicRepoCount: snapshot.publicRepoCount,
    followersCount: snapshot.followersCount ?? null,
    followingCount: snapshot.followingCount ?? null,
    totalStars: snapshot.totalStars ?? null,
    totalCommits: snapshot.totalCommits ?? null,
    rawPayloadText: snapshot.rawPayload ? JSON.stringify(snapshot.rawPayload, null, 2) : '',
    contributionDaysText: JSON.stringify(snapshot.contributionDays, null, 2),
  };
}
