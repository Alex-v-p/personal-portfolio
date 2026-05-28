export interface ContactMethod {
  id: string;
  platform: string;
  label: string;
  value: string;
  href: string;
  actionLabel: string;
  iconKey?: string;
  description?: string;
  sortOrder: number;
  isVisible: boolean;
}
