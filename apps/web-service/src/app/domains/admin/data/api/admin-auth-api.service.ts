import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminAuthToken, AdminUser } from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminAuthApiService {
  private readonly adminHttp = inject(AdminHttpService);

  login(email: string, password: string): Observable<AdminAuthToken> {
    return this.adminHttp.http.post<AdminAuthToken>(this.adminHttp.adminUrl('auth/login'), { email, password });
  }

  getCurrentAdmin(): Observable<AdminUser> {
    return this.adminHttp.http.get<AdminUser>(this.adminHttp.adminUrl('auth/me'));
  }
}
