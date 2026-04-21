import { ResolvedMedia } from '@domains/media/model/resolved-media.model';

export interface AdminSocialLink {
  id?: string | null;
  platform: string;
  label: string;
  url: string;
  iconKey?: string | null;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminProfile {
  id: string;
  firstName: string;
  lastName: string;
  headline: string;
  headlineNl?: string | null;
  shortIntro: string;
  shortIntroNl?: string | null;
  longBio?: string | null;
  longBioNl?: string | null;
  location?: string | null;
  email?: string | null;
  phone?: string | null;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  avatar?: ResolvedMedia | null;
  heroImage?: ResolvedMedia | null;
  resume?: ResolvedMedia | null;
  ctaPrimaryLabel?: string | null;
  ctaPrimaryLabelNl?: string | null;
  ctaPrimaryUrl?: string | null;
  ctaSecondaryLabel?: string | null;
  ctaSecondaryLabelNl?: string | null;
  ctaSecondaryUrl?: string | null;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
  createdAt: string;
  updatedAt: string;
}

export interface AdminProfileUpdate {
  firstName: string;
  lastName: string;
  headline: string;
  headlineNl?: string | null;
  shortIntro: string;
  shortIntroNl?: string | null;
  longBio?: string | null;
  longBioNl?: string | null;
  location?: string | null;
  email?: string | null;
  phone?: string | null;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  ctaPrimaryLabel?: string | null;
  ctaPrimaryLabelNl?: string | null;
  ctaPrimaryUrl?: string | null;
  ctaSecondaryLabel?: string | null;
  ctaSecondaryLabelNl?: string | null;
  ctaSecondaryUrl?: string | null;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
}
