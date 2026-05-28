export interface AdminNavigationItem {
  id: string;
  label: string;
  labelNl?: string | null;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}

export interface AdminNavigationItemUpsert {
  label: string;
  labelNl?: string | null;
  routePath: string;
  isExternal: boolean;
  sortOrder: number;
  isVisible: boolean;
}
