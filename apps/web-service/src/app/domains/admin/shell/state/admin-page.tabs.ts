export const ADMIN_TABS = [
  { id: 'projects', label: 'Projects' },
  { id: 'taxonomy', label: 'Taxonomy' },
  { id: 'experience', label: 'Experience' },
  { id: 'navigation', label: 'Navigation' },
  { id: 'admins', label: 'Admin users' },
] as const;

export type AdminVisibleTabId = typeof ADMIN_TABS[number]['id'];
export type AdminTabId =
  | 'overview'
  | 'projects'
  | 'blog'
  | 'media'
  | 'messages'
  | 'activity'
  | 'assistant'
  | 'profile'
  | 'stats'
  | 'taxonomy'
  | 'experience'
  | 'navigation'
  | 'admins';
