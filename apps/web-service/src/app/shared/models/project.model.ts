export interface ProjectLink {
  label: string;
  href?: string;
  routerLink?: string | readonly string[];
}

export interface Project {
  id: string;
  slug: string;
  title: string;
  shortDescription: string;
  summary: string;
  organization: string;
  duration: string;
  status: 'Completed' | 'In progress' | 'Planned';
  category: string;
  tags: string[];
  featured: boolean;
  imageAlt: string;
  highlight: string;
  links: ProjectLink[];
}
