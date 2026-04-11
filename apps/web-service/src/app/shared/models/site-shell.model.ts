import { ContactMethod } from './contact-method.model';
import { Profile } from './profile.model';

export interface NavigationItem {
  id: string;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface SiteShellData {
  navigation: NavigationItem[];
  profile: Profile;
  footerText: string;
  contactMethods: ContactMethod[];
}
