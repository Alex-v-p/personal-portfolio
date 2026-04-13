import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { AdminAssistantKnowledgeStatus, AdminDashboardSummary, AdminReferenceData, AdminSiteActivity } from '../../models/admin.model';
import { AdminHttpService } from './admin-http.service';

@Injectable({ providedIn: 'root' })
export class AdminOverviewApiService {
  private readonly adminHttp = inject(AdminHttpService);

  getDashboardSummary(): Observable<AdminDashboardSummary> {
    return this.adminHttp.http.get<AdminDashboardSummary>(this.adminHttp.adminUrl('dashboard'));
  }

  getReferenceData(): Observable<AdminReferenceData> {
    return this.adminHttp.http.get<AdminReferenceData>(this.adminHttp.adminUrl('reference-data'));
  }

  getAssistantKnowledgeStatus(): Observable<AdminAssistantKnowledgeStatus> {
    return this.adminHttp.http.get<AdminAssistantKnowledgeStatus>(this.adminHttp.adminUrl('assistant/knowledge'));
  }

  getSiteActivity(): Observable<AdminSiteActivity> {
    return this.adminHttp.http.get<AdminSiteActivity>(this.adminHttp.adminUrl('site-activity'));
  }

  rebuildAssistantKnowledge(): Observable<AdminAssistantKnowledgeStatus> {
    return this.adminHttp.http.post<AdminAssistantKnowledgeStatus>(this.adminHttp.adminUrl('assistant/knowledge/rebuild'), {});
  }
}
