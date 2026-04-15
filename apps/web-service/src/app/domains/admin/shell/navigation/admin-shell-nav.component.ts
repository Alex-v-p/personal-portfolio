import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { ADMIN_SHELL_NAV_ITEMS } from './admin-shell.navigation';

@Component({
  selector: 'app-admin-shell-nav',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <nav class="rounded-[2rem] border border-stone-300 bg-white p-4 shadow-[0_20px_45px_rgba(40,31,20,0.08)] sm:p-5 lg:px-6">
      <div class="grid gap-4 xl:grid-cols-[18rem_minmax(0,1fr)] xl:items-start">
        <div class="space-y-1.5">
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-stone-500">CMS workspaces</p>
          <p class="text-sm text-stone-600">Jump between content, operations, and system areas.</p>
        </div>

        <div class="flex flex-wrap gap-2.5 xl:justify-end">
          <a
            *ngFor="let item of navItems"
            [routerLink]="item.path"
            routerLinkActive="bg-stone-900 text-white shadow-[0_10px_25px_rgba(40,31,20,0.14)]"
            [routerLinkActiveOptions]="{ exact: true }"
            class="inline-flex min-h-11 items-center rounded-full bg-stone-100 px-4 text-sm font-semibold text-stone-700 transition hover:bg-stone-200"
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
