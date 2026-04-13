import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminProfile, AdminProfileUpdate } from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminProfileApiService {
  private readonly adminHttp = inject(AdminHttpService);

  getProfile(): Observable<AdminProfile> {
    return this.adminHttp.http.get<AdminProfile>(this.adminHttp.adminUrl('profile'));
  }

  updateProfile(payload: AdminProfileUpdate): Observable<AdminProfile> {
    return this.adminHttp.http.put<AdminProfile>(this.adminHttp.adminUrl('profile'), payload);
  }
}
