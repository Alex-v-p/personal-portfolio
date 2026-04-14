import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize, map, tap } from 'rxjs/operators';

import {
  AdminAuthSession,
  AdminMfaSetupChallenge,
  AdminMfaSetupConfirmResult,
  AdminUser,
} from '@domains/admin/model/admin.model';
import { AdminAuthApiService } from '@domains/admin/data/api/admin-auth-api.service';

const AUTH_SESSION_STORAGE_KEY = 'portfolio.admin.auth-session';

@Injectable({ providedIn: 'root' })
export class AdminSessionService {
  private readonly router = inject(Router);
  private readonly authApi = inject(AdminAuthApiService);
  private readonly sessionSubject = new BehaviorSubject<AdminAuthSession | null>(this.readStoredSession());

  readonly authSession$ = this.sessionSubject.asObservable();

  get currentSession(): AdminAuthSession | null {
    return this.sessionSubject.value;
  }

  get currentUser(): AdminUser | null {
    return this.currentSession?.user ?? null;
  }

  get currentUser$(): Observable<AdminUser | null> {
    return this.authSession$.pipe(map((session) => session?.user ?? null));
  }

  get csrfToken(): string | null {
    return this.currentSession?.csrfToken ?? null;
  }

  get isAuthenticated(): boolean {
    return !!this.currentUser;
  }

  get isFullyAuthenticated(): boolean {
    return !!this.currentSession && this.currentSession.isMfaVerified && !this.currentSession.mfaRequired && !this.currentSession.mfaSetupRequired;
  }

  get hasPendingMfaStep(): boolean {
    return !!this.currentSession && (this.currentSession.mfaRequired || this.currentSession.mfaSetupRequired);
  }

  get requiresMfaSetup(): boolean {
    return !!this.currentSession?.mfaSetupRequired;
  }

  get requiresMfaVerification(): boolean {
    return !!this.currentSession?.mfaRequired;
  }

  login(email: string, password: string): Observable<AdminAuthSession> {
    return this.authApi.login(email, password).pipe(tap((authSession) => this.storeSession(authSession)));
  }

  restoreSession(): Observable<AdminAuthSession | null> {
    return this.authApi.getCurrentAdmin().pipe(
      tap((authSession) => this.storeSession(authSession)),
      catchError(() => {
        this.clearSession(false);
        return of(null);
      }),
    );
  }

  beginMfaSetup(): Observable<AdminMfaSetupChallenge> {
    return this.authApi.beginMfaSetup();
  }

  confirmMfaSetup(code: string): Observable<AdminMfaSetupConfirmResult> {
    return this.authApi.confirmMfaSetup(code).pipe(
      tap((result) => this.storeSession(result.session)),
    );
  }

  verifyMfa(code: string | null, recoveryCode: string | null): Observable<AdminAuthSession> {
    return this.authApi.verifyMfa({ code, recoveryCode }).pipe(
      tap((authSession) => this.storeSession(authSession)),
    );
  }

  logout(redirectToLogin = true): void {
    this.authApi.logout().pipe(
      catchError(() => of(void 0)),
      finalize(() => {
        this.clearSession(redirectToLogin);
      }),
    ).subscribe();
  }

  private storeSession(authSession: AdminAuthSession): void {
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.setItem(AUTH_SESSION_STORAGE_KEY, JSON.stringify(authSession));
    }
    this.sessionSubject.next(authSession);
  }

  private clearSession(redirectToLogin: boolean): void {
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.removeItem(AUTH_SESSION_STORAGE_KEY);
    }
    this.sessionSubject.next(null);
    if (redirectToLogin) {
      void this.router.navigate(['/admin/login']);
    }
  }

  private readStoredSession(): AdminAuthSession | null {
    if (typeof sessionStorage === 'undefined') {
      return null;
    }
    const raw = sessionStorage.getItem(AUTH_SESSION_STORAGE_KEY);
    if (!raw) {
      return null;
    }
    try {
      return JSON.parse(raw) as AdminAuthSession;
    } catch {
      return null;
    }
  }
}
