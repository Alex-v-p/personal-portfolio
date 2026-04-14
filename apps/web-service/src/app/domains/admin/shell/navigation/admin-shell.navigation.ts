export interface AdminShellNavItem {
  path: string;
  label: string;
}

export const ADMIN_SHELL_NAV_ITEMS: AdminShellNavItem[] = [
  { path: 'overview', label: 'Overview' },
  { path: 'messages', label: 'Messages' },
  { path: 'projects', label: 'Projects' },
  { path: 'blog', label: 'Blog' },
  { path: 'media', label: 'Media' },
  { path: 'taxonomy', label: 'Taxonomy' },
  { path: 'experience', label: 'Experience' },
  { path: 'navigation', label: 'Navigation' },
  { path: 'profile', label: 'Profile' },
  { path: 'stats', label: 'GitHub / Stats' },
  { path: 'assistant', label: 'Assistant' },
  { path: 'activity', label: 'Activity' },
  { path: 'admins', label: 'Admin users' },
];
