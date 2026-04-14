import { CollectionResponse, ExpertiseGroupApi, MediaApi } from './common.contracts';

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

export interface SiteShellApi {
  navigation: CollectionResponse<NavigationItemApi>;
  profile: ProfileApi;
  footerText: string;
  contactMethods: ContactMethodApi[];
}
