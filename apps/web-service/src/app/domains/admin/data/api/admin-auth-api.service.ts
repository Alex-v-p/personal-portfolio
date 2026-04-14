import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminAuthSession } from '@domains/admin/model/admin.model';
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

  logout(): Observable<void> {
    return this.adminHttp.http.post<void>(this.adminHttp.adminUrl('auth/logout'), {}, { withCredentials: true });
  }
}
