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
  name: string;
  role: string;
  greeting: string;
  location: string;
  heroTitle: string;
  summary: string;
  shortBio: string;
  footerDescription: string;
  skills: string[];
  expertiseGroups: ExpertiseGroup[];
  introParagraphs: string[];
  availability: string[];
  heroActions: HeroAction[];
}
