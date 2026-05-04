import { HttpErrorResponse } from '@angular/common/http';
import { NgIf } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize, take } from 'rxjs/operators';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';

@Component({
  selector: 'app-admin-login-page',
  standalone: true,
  imports: [NgIf, FormsModule],
  templateUrl: './admin-login.page.html'
})
export class AdminLoginPageComponent {
  private readonly adminSession = inject(AdminSessionService);
  private readonly router = inject(Router);

  protected email = '';
  protected password = '';
  protected isSubmitting = false;
  protected errorMessage = '';

  protected submit(): void {
    this.isSubmitting = true;
    this.errorMessage = '';

    this.adminSession.login(this.email.trim(), this.password).pipe(
      take(1),
      finalize(() => {
        this.isSubmitting = false;
      })
    ).subscribe({
      next: async (authSession) => {
        if (authSession.mfaRequired || authSession.mfaSetupRequired) {
          await this.router.navigate(['/admin/mfa']);
          return;
        }
        await this.router.navigate(['/admin']);
      },
      error: (error: unknown) => {
        if (error instanceof HttpErrorResponse && error.status === 429) {
          this.errorMessage = 'Too many login attempts. Please wait a moment and try again.';
          return;
        }
        this.errorMessage = 'Admin login failed. Check your credentials and try again.';
      }
    });
  }
}
