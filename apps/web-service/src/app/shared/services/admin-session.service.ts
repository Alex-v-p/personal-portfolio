import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { AdminAuthToken, AdminUser } from '../models/admin.model';
import { AdminPortfolioApiService } from './admin-portfolio-api.service';

const TOKEN_STORAGE_KEY = 'portfolio.admin.access-token';
const USER_STORAGE_KEY = 'portfolio.admin.user';

@Injectable({ providedIn: 'root' })
export class AdminSessionService {
  private readonly router = inject(Router);
  private readonly adminApi = inject(AdminPortfolioApiService);
  private readonly currentUserSubject = new BehaviorSubject<AdminUser | null>(this.readStoredUser());

  readonly currentUser$ = this.currentUserSubject.asObservable();

  get currentUser(): AdminUser | null {
    return this.currentUserSubject.value;
  }

  get token(): string | null {
    if (typeof localStorage === 'undefined') {
      return null;
    }
    return localStorage.getItem(TOKEN_STORAGE_KEY);
  }

  get isAuthenticated(): boolean {
    return !!this.token;
  }

  login(email: string, password: string): Observable<AdminUser> {
    return this.adminApi.login(email, password).pipe(
      tap((auth) => this.storeAuth(auth)),
      map((auth) => auth.user)
    );
  }

  restoreSession(): Observable<AdminUser | null> {
    if (!this.token) {
      return of(null);
    }

    return this.adminApi.getCurrentAdmin().pipe(
      tap((user) => this.storeUser(user)),
      map((user) => user as AdminUser | null),
      catchError((error) => {
        this.logout(false);
        return throwError(() => error);
      })
    );
  }

  logout(redirectToLogin = true): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem(USER_STORAGE_KEY);
    }
    this.currentUserSubject.next(null);
    if (redirectToLogin) {
      void this.router.navigate(['/admin/login']);
    }
  }

  private storeAuth(auth: AdminAuthToken): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(TOKEN_STORAGE_KEY, auth.accessToken);
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(auth.user));
    }
    this.currentUserSubject.next(auth.user);
  }

  private storeUser(user: AdminUser): void {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    }
    this.currentUserSubject.next(user);
  }

  private readStoredUser(): AdminUser | null {
    if (typeof localStorage === 'undefined') {
      return null;
    }
    const raw = localStorage.getItem(USER_STORAGE_KEY);
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
