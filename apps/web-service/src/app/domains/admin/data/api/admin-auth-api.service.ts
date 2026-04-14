import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import {
  AdminAuthSession,
  AdminMfaSetupChallenge,
  AdminMfaSetupConfirmResult,
} from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminAuthApiService {
  private readonly adminHttp = inject(AdminHttpService);

  login(email: string, password: string): Observable<AdminAuthSession> {
    return this.adminHttp.http.post<AdminAuthSession>(this.adminHttp.adminUrl('auth/login'), { email, password }, { withCredentials: true });
  }

  getCurrentAdmin(): Observable<AdminAuthSession> {
    return this.adminHttp.http.get<AdminAuthSession>(this.adminHttp.adminUrl('auth/me'), { withCredentials: true });
  }

  beginMfaSetup(): Observable<AdminMfaSetupChallenge> {
    return this.adminHttp.http.post<AdminMfaSetupChallenge>(this.adminHttp.adminUrl('auth/mfa/setup'), {}, { withCredentials: true });
  }

  confirmMfaSetup(code: string): Observable<AdminMfaSetupConfirmResult> {
    return this.adminHttp.http.post<AdminMfaSetupConfirmResult>(
      this.adminHttp.adminUrl('auth/mfa/setup/confirm'),
      { code },
      { withCredentials: true },
    );
  }

  verifyMfa(payload: { code?: string | null; recoveryCode?: string | null }): Observable<AdminAuthSession> {
    return this.adminHttp.http.post<AdminAuthSession>(this.adminHttp.adminUrl('auth/mfa/verify'), payload, { withCredentials: true });
  }

  logout(): Observable<void> {
    return this.adminHttp.http.post<void>(this.adminHttp.adminUrl('auth/logout'), {}, { withCredentials: true });
  }
}
