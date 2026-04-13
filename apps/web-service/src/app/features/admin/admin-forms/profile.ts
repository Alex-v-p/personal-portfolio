import { AdminProfile, AdminSocialLink } from '../../../shared/models/admin.model';

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
