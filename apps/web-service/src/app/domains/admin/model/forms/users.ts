import { AdminUser } from '@domains/admin/model/admin.model';

export interface AdminUserForm {
  id?: string | null;
  email: string;
  displayName: string;
  password: string;
  isActive: boolean;
}

export function createEmptyAdminUserForm(): AdminUserForm {
  return { email: '', displayName: '', password: '', isActive: true };
}

export function toAdminUserForm(user: AdminUser): AdminUserForm {
  return { id: user.id, email: user.email, displayName: user.displayName, password: '', isActive: user.isActive };
}
