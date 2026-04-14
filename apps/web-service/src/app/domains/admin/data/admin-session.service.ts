import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize, map, tap } from 'rxjs/operators';

import { AdminAuthSession, AdminUser } from '@domains/admin/model/admin.model';
import { AdminAuthApiService } from '@domains/admin/data/api/admin-auth-api.service';

const USER_STORAGE_KEY = 'portfolio.admin.user';
const CSRF_STORAGE_KEY = 'portfolio.admin.csrf-token';

@Injectable({ providedIn: 'root' })
export class AdminSessionService {
  private readonly router = inject(Router);
  private readonly authApi = inject(AdminAuthApiService);
  private readonly currentUserSubject = new BehaviorSubject<AdminUser | null>(this.readStoredUser());

  readonly currentUser$ = this.currentUserSubject.asObservable();

  get currentUser(): AdminUser | null {
    return this.currentUserSubject.value;
  }

  get csrfToken(): string | null {
    if (typeof sessionStorage === 'undefined') {
      return null;
    }
    return sessionStorage.getItem(CSRF_STORAGE_KEY);
  }

  get isAuthenticated(): boolean {
    return !!this.currentUser;
  }

  login(email: string, password: string): Observable<AdminUser> {
    return this.authApi.login(email, password).pipe(
      tap((authSession) => this.storeSession(authSession)),
      map((authSession) => authSession.user)
    );
  }

  restoreSession(): Observable<AdminUser | null> {
    return this.authApi.getCurrentAdmin().pipe(
      tap((authSession) => this.storeSession(authSession)),
      map((authSession) => authSession.user as AdminUser | null),
      catchError(() => {
        this.clearSession(false);
        return of(null);
      })
    );
  }

  logout(redirectToLogin = true): void {
    this.authApi.logout().pipe(
      catchError(() => of(void 0)),
      finalize(() => {
        this.clearSession(redirectToLogin);
      })
    ).subscribe();
  }

  private storeSession(authSession: AdminAuthSession): void {
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.setItem(USER_STORAGE_KEY, JSON.stringify(authSession.user));
      sessionStorage.setItem(CSRF_STORAGE_KEY, authSession.csrfToken);
    }
    this.currentUserSubject.next(authSession.user);
  }

  private clearSession(redirectToLogin: boolean): void {
    if (typeof sessionStorage !== 'undefined') {
      sessionStorage.removeItem(USER_STORAGE_KEY);
      sessionStorage.removeItem(CSRF_STORAGE_KEY);
    }
    this.currentUserSubject.next(null);
    if (redirectToLogin) {
      void this.router.navigate(['/admin/login']);
    }
  }

  private readStoredUser(): AdminUser | null {
    if (typeof sessionStorage === 'undefined') {
      return null;
    }
    const raw = sessionStorage.getItem(USER_STORAGE_KEY);
    if (!raw) {
      return null;
    }
    try {
      return JSON.parse(raw) as AdminUser;
    } catch {
      return null;
    }
  }
}
