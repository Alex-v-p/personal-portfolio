export const ADMIN_TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'media', label: 'Media' },
  { id: 'projects', label: 'Projects' },
  { id: 'blog', label: 'Blog' },
  { id: 'taxonomy', label: 'Taxonomy' },
  { id: 'experience', label: 'Experience' },
  { id: 'navigation', label: 'Navigation' },
  { id: 'profile', label: 'Profile' },
  { id: 'stats', label: 'GitHub / Stats' },
  { id: 'assistant', label: 'Assistant' },
  { id: 'activity', label: 'Activity' },
  { id: 'admins', label: 'Admin users' },
  { id: 'messages', label: 'Messages' },
] as const;

export type AdminTabId = typeof ADMIN_TABS[number]['id'];
