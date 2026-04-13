import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminCollectionResponse, AdminContactMessage, AdminUser, AdminUserCreate, AdminUserUpdate } from '../../models/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminMessagesApiService {
  private readonly adminHttp = inject(AdminHttpService);

  getContactMessages(): Observable<AdminCollectionResponse<AdminContactMessage>> {
    return this.adminHttp.http.get<AdminCollectionResponse<AdminContactMessage>>(this.adminHttp.adminUrl('contact-messages'));
  }

  updateContactMessage(messageId: string, isRead: boolean): Observable<AdminContactMessage> {
    return this.adminHttp.http.patch<AdminContactMessage>(this.adminHttp.adminUrl(`contact-messages/${messageId}`), { isRead });
  }

  listAdminUsers(): Observable<AdminUser[]> {
    return this.adminHttp.http.get<AdminUser[]>(this.adminHttp.adminUrl('admin-users'));
  }

  createAdminUser(payload: AdminUserCreate): Observable<AdminUser> {
    return this.adminHttp.http.post<AdminUser>(this.adminHttp.adminUrl('admin-users'), payload);
  }

  updateAdminUser(adminUserId: string, payload: AdminUserUpdate): Observable<AdminUser> {
    return this.adminHttp.http.put<AdminUser>(this.adminHttp.adminUrl(`admin-users/${adminUserId}`), payload);
  }

  deleteAdminUser(adminUserId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`admin-users/${adminUserId}`));
  }
}
