export interface AdminShellNavItem {
  path: string;
  label: string;
}

export const ADMIN_SHELL_NAV_ITEMS: AdminShellNavItem[] = [
  { path: 'overview', label: 'Overview' },
  { path: 'profile', label: 'Profile' },
  { path: 'navigation', label: 'Navigation' },
  { path: 'experience', label: 'Experience' },
  { path: 'projects', label: 'Projects' },
  { path: 'blog', label: 'Blog' },
  { path: 'messages', label: 'Messages' },
  { path: 'stats', label: 'GitHub / Stats' },
  { path: 'assistant', label: 'Assistant' },
  { path: 'media', label: 'Media' },
  { path: 'taxonomy', label: 'Taxonomy' },
  { path: 'activity', label: 'Activity' },
  { path: 'admins', label: 'Admin users' },
];
