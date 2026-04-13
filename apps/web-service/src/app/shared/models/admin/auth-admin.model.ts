export interface AdminUser {
  id: string;
  email: string;
  displayName: string;
  isActive: boolean;
  createdAt: string;
}

export interface AdminUserCreate {
  email: string;
  displayName: string;
  password: string;
  isActive: boolean;
}

export interface AdminUserUpdate {
  email: string;
  displayName: string;
  password?: string | null;
  isActive: boolean;
}

export interface AdminAuthToken {
  accessToken: string;
  tokenType: string;
  expiresInSeconds: number;
  user: AdminUser;
}
