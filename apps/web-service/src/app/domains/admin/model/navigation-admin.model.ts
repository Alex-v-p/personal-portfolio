export interface AdminNavigationItem {
  id: string;
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminNavigationItemUpsert {
  label: string;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}
