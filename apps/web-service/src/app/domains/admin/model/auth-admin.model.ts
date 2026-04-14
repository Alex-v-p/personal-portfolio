export interface AdminUser {
  id: string;
  email: string;
  displayName: string;
  isActive: boolean;
  createdAt: string;
  mfaEnabled?: boolean;
  mfaEnrolledAt?: string | null;
  mfaRecoveryCodesRemaining?: number;
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

export interface AdminAuthSession {
  csrfToken: string;
  expiresInSeconds: number;
  user: AdminUser;
  isMfaEnabled: boolean;
  isMfaVerified: boolean;
  mfaRequired: boolean;
  mfaSetupRequired: boolean;
}

export interface AdminMfaSetupChallenge {
  manualEntryKey: string;
  otpauthUri: string;
  qrCodeDataUrl: string;
  issuer: string;
}

export interface AdminMfaSetupConfirmResult {
  backupCodes: string[];
  session: AdminAuthSession;
}
