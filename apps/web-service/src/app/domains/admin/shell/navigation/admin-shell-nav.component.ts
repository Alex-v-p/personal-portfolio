import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

import { ADMIN_SHELL_NAV_ITEMS } from './admin-shell.navigation';

@Component({
  selector: 'app-admin-shell-nav',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  template: `
    <nav class="flex flex-wrap gap-3 rounded-[2rem] border border-stone-300 bg-white p-4 shadow-[0_20px_45px_rgba(40,31,20,0.08)]">
      <a
        *ngFor="let item of navItems"
        [routerLink]="item.path"
        routerLinkActive="bg-stone-900 text-white"
        [routerLinkActiveOptions]="{ exact: true }"
        class="inline-flex min-h-11 items-center rounded-full bg-stone-100 px-4 text-sm font-semibold text-stone-700 transition hover:bg-stone-200"
      >
        {{ item.label }}
      </a>
    </nav>
  `,
})
export class AdminShellNavComponent {
  protected readonly navItems = ADMIN_SHELL_NAV_ITEMS;
}
