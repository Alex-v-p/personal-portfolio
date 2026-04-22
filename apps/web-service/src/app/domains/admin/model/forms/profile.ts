import { AdminProfile, AdminSocialLink } from '@domains/admin/model/admin.model';

export interface AdminProfileForm {
  id?: string;
  firstName: string;
  lastName: string;
  headline: string;
  headlineNl: string;
  shortIntro: string;
  shortIntroNl: string;
  longBio: string;
  longBioNl: string;
  location: string;
  email: string;
  phone: string;
  avatarFileId: string | null;
  heroImageFileId: string | null;
  resumeFileId: string | null;
  ctaPrimaryLabel: string;
  ctaPrimaryLabelNl: string;
  ctaPrimaryUrl: string;
  ctaSecondaryLabel: string;
  ctaSecondaryLabelNl: string;
  ctaSecondaryUrl: string;
  isPublic: boolean;
  socialLinks: AdminSocialLink[];
}

export function createEmptyProfileForm(): AdminProfileForm {
  return {
    firstName: '',
    lastName: '',
    headline: '',
    headlineNl: '',
    shortIntro: '',
    shortIntroNl: '',
    longBio: '',
    longBioNl: '',
    location: '',
    email: '',
    phone: '',
    avatarFileId: null,
    heroImageFileId: null,
    resumeFileId: null,
    ctaPrimaryLabel: '',
    ctaPrimaryLabelNl: '',
    ctaPrimaryUrl: '',
    ctaSecondaryLabel: '',
    ctaSecondaryLabelNl: '',
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
    headlineNl: profile.headlineNl ?? '',
    shortIntro: profile.shortIntro,
    shortIntroNl: profile.shortIntroNl ?? '',
    longBio: profile.longBio ?? '',
    longBioNl: profile.longBioNl ?? '',
    location: profile.location ?? '',
    email: profile.email ?? '',
    phone: profile.phone ?? '',
    avatarFileId: profile.avatarFileId ?? null,
    heroImageFileId: profile.heroImageFileId ?? null,
    resumeFileId: profile.resumeFileId ?? null,
    ctaPrimaryLabel: profile.ctaPrimaryLabel ?? '',
    ctaPrimaryLabelNl: profile.ctaPrimaryLabelNl ?? '',
    ctaPrimaryUrl: profile.ctaPrimaryUrl ?? '',
    ctaSecondaryLabel: profile.ctaSecondaryLabel ?? '',
    ctaSecondaryLabelNl: profile.ctaSecondaryLabelNl ?? '',
    ctaSecondaryUrl: profile.ctaSecondaryUrl ?? '',
    isPublic: profile.isPublic,
    socialLinks: profile.socialLinks.map((link) => ({ ...link })),
  };
}
