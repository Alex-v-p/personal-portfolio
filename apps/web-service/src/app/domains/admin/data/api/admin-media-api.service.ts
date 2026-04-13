import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminMediaApiService {
  private readonly adminHttp = inject(AdminHttpService);

  listMediaFiles(): Observable<AdminMediaFile[]> {
    return this.adminHttp.http.get<AdminMediaFile[]>(this.adminHttp.adminUrl('media-files'));
  }

  uploadMedia(formData: FormData): Observable<AdminMediaFile> {
    return this.adminHttp.http.post<AdminMediaFile>(this.adminHttp.adminUrl('media-files/upload'), formData);
  }

  deleteMediaFile(mediaId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`media-files/${mediaId}`));
  }
}
