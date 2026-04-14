export const ADMIN_TABS = [
  { id: 'projects', label: 'Projects' },
  { id: 'taxonomy', label: 'Taxonomy' },
  { id: 'experience', label: 'Experience' },
  { id: 'navigation', label: 'Navigation' },
  { id: 'profile', label: 'Profile' },
  { id: 'stats', label: 'GitHub / Stats' },
  { id: 'assistant', label: 'Assistant' },
  { id: 'admins', label: 'Admin users' },
] as const;

export type AdminTabId = typeof ADMIN_TABS[number]['id'];
