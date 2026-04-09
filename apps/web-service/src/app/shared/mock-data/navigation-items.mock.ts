import { NavigationItem } from '../models/navigation-item.model';

export const NAVIGATION_ITEMS: NavigationItem[] = [
  { id: 'nav-home', label: 'Home', routePath: '/', isExternal: false, sortOrder: 1, isVisible: true },
  { id: 'nav-projects', label: 'Projects', routePath: '/projects', isExternal: false, sortOrder: 2, isVisible: true },
  { id: 'nav-blog', label: 'Blog', routePath: '/blog', isExternal: false, sortOrder: 3, isVisible: true },
  { id: 'nav-contact', label: 'Contact', routePath: '/contact', isExternal: false, sortOrder: 4, isVisible: true },
  { id: 'nav-stats', label: 'Stats', routePath: '/stats', isExternal: false, sortOrder: 5, isVisible: true },
  { id: 'nav-assistant', label: 'Assistant', routePath: '/assistant', isExternal: false, sortOrder: 6, isVisible: false }
].sort((a, b) => a.sortOrder - b.sortOrder);
