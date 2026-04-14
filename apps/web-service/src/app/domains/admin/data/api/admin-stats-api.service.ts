import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminAsyncTaskAccepted, AdminGithubSnapshot, AdminGithubSnapshotRefreshRequest, AdminGithubSnapshotsResponse, AdminGithubSnapshotUpsert } from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminStatsApiService {
  private readonly adminHttp = inject(AdminHttpService);

  getGithubSnapshots(): Observable<AdminGithubSnapshotsResponse> {
    return this.adminHttp.http.get<AdminGithubSnapshotsResponse>(this.adminHttp.adminUrl('github-snapshots'));
  }

  createGithubSnapshot(payload: AdminGithubSnapshotUpsert): Observable<AdminGithubSnapshot> {
    return this.adminHttp.http.post<AdminGithubSnapshot>(this.adminHttp.adminUrl('github-snapshots'), payload);
  }

  refreshGithubSnapshot(payload: AdminGithubSnapshotRefreshRequest): Observable<AdminGithubSnapshot | AdminAsyncTaskAccepted> {
    return this.adminHttp.http.post<AdminGithubSnapshot | AdminAsyncTaskAccepted>(this.adminHttp.adminUrl('github-snapshots/refresh'), payload);
  }

  updateGithubSnapshot(snapshotId: string, payload: AdminGithubSnapshotUpsert): Observable<AdminGithubSnapshot> {
    return this.adminHttp.http.put<AdminGithubSnapshot>(this.adminHttp.adminUrl(`github-snapshots/${snapshotId}`), payload);
  }

  deleteGithubSnapshot(snapshotId: string): Observable<void> {
    return this.adminHttp.http.delete<void>(this.adminHttp.adminUrl(`github-snapshots/${snapshotId}`));
  }
}
