import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminBackupImportResult } from '@domains/admin/model/backup-admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminBackupApiService {
  private readonly adminHttp = inject(AdminHttpService);

  exportBackup(): Observable<Blob> {
    return this.adminHttp.http.get(this.adminHttp.adminUrl('backup/export'), { responseType: 'blob' });
  }

  importBackup(file: File, replaceExisting = true): Observable<AdminBackupImportResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('replaceExisting', String(replaceExisting));
    return this.adminHttp.http.post<AdminBackupImportResult>(this.adminHttp.adminUrl('backup/import'), formData);
  }
}
