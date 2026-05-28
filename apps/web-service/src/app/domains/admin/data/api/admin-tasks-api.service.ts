import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminAsyncTaskStatus } from '@domains/admin/model/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminTasksApiService {
  private readonly adminHttp = inject(AdminHttpService);

  getTask(taskId: string): Observable<AdminAsyncTaskStatus> {
    return this.adminHttp.http.get<AdminAsyncTaskStatus>(this.adminHttp.adminUrl(`tasks/${taskId}`));
  }
}
