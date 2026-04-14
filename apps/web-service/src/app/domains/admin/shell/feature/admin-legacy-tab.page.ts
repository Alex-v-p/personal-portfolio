import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { AdminPageComponent } from '@domains/admin/shell/feature/admin.page';
import { AdminTabId } from '@domains/admin/shell/state/admin-page.tabs';

@Component({
  selector: 'app-admin-legacy-tab-page',
  standalone: true,
  imports: [CommonModule, AdminPageComponent],
  template: `
    <app-admin-page
      [initialTab]="initialTab"
      [compactMode]="true">
    </app-admin-page>
  `,
})
export class AdminLegacyTabPageComponent {
  private readonly route = inject(ActivatedRoute);

  protected readonly initialTab = (this.route.snapshot.data['legacyTab'] as AdminTabId | undefined) ?? 'projects';
}
