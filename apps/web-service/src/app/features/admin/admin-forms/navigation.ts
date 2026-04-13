import { AdminNavigationItem } from '../../../shared/models/admin.model';

export interface AdminNavigationItemForm {
  id?: string | null;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export function createEmptyNavigationItemForm(): AdminNavigationItemForm {
  return { label: '', routePath: '', isExternal: false, sortOrder: 0, isVisible: true };
}

export function toNavigationItemForm(item: AdminNavigationItem): AdminNavigationItemForm {
  return {
    id: item.id,
    label: item.label,
    routePath: item.routePath,
    isExternal: item.isExternal,
    sortOrder: item.sortOrder,
    isVisible: item.isVisible,
  };
}
