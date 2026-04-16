import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { ADMIN_SHELL_NAV_ITEMS } from './admin-shell.navigation';

@Component({
  selector: 'app-admin-shell-nav',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <nav class="p-0">
      <div class="grid gap-4 xl:grid-cols-[18rem_minmax(0,1fr)] xl:items-start">
        <div class="space-y-1.5">
          <p class="ui-kicker">CMS workspaces</p>
          <p class="text-sm ui-text-muted">Jump between content, operations, and system areas.</p>
        </div>

        <div class="flex flex-wrap gap-2.5 xl:justify-end">
          <a
            *ngFor="let item of navItems"
            [routerLink]="item.path"
            routerLinkActive="ui-tab-pill-active"
            [routerLinkActiveOptions]="{ exact: true }"
            class="ui-tab-pill"
          >
            {{ item.label }}
          </a>
        </div>
      </div>
    </nav>
  `,
})
export class AdminShellNavComponent {
  protected readonly navItems = ADMIN_SHELL_NAV_ITEMS;
}