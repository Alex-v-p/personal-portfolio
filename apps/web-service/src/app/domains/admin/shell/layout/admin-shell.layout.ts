import { Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminShellNavComponent } from '@domains/admin/shell/navigation/admin-shell-nav.component';

@Component({
  selector: 'app-admin-shell-layout',
  standalone: true,
  imports: [RouterOutlet, AdminShellNavComponent],
  templateUrl: './admin-shell.layout.html',
})
export class AdminShellLayoutComponent {
  private readonly adminSession = inject(AdminSessionService);

  protected get adminDisplayName(): string {
    return this.adminSession.currentUser?.displayName ?? 'Admin';
  }

  protected logout(): void {
    this.adminSession.logout();
  }
}
