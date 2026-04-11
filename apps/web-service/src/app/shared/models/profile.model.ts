import { SocialLink } from './social-link.model';

export interface HeroAction {
  label: string;
  appearance: 'primary' | 'secondary' | 'ghost';
  href?: string;
  routerLink?: string | readonly string[];
  openInNewTab?: boolean;
}

export interface ExpertiseGroup {
  title: string;
  tags: string[];
}

export interface Profile {
  id: string;
  firstName: string;
  lastName: string;
  name: string;
  headline: string;
  role: string;
  greeting: string;
  location: string;
  email: string;
  phone: string;
  shortIntro: string;
  longBio: string;
  heroTitle: string;
  summary: string;
  shortBio: string;
  footerDescription: string;
  avatarFileId?: string | null;
  heroImageFileId?: string | null;
  resumeFileId?: string | null;
  avatarUrl?: string;
  heroImageUrl?: string;
  resumeUrl?: string;
  skills: string[];
  expertiseGroups: ExpertiseGroup[];
  introParagraphs: string[];
  availability: string[];
  heroActions: HeroAction[];
  socialLinks?: SocialLink[];
  createdAt?: string;
  updatedAt?: string;
}
