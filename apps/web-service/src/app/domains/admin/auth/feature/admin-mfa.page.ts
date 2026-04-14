import { HttpErrorResponse } from '@angular/common/http';
import { NgFor, NgIf } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { finalize, take } from 'rxjs/operators';

import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminMfaSetupChallenge } from '@domains/admin/model/admin.model';

@Component({
  selector: 'app-admin-mfa-page',
  standalone: true,
  imports: [NgIf, NgFor, FormsModule],
  templateUrl: './admin-mfa.page.html',
})
export class AdminMfaPageComponent implements OnInit {
  private readonly adminSession = inject(AdminSessionService);
  private readonly router = inject(Router);

  protected setupChallenge: AdminMfaSetupChallenge | null = null;
  protected setupCode = '';
  protected loginCode = '';
  protected recoveryCode = '';
  protected backupCodes: string[] = [];
  protected useRecoveryCode = false;
  protected isBusy = false;
  protected isLoadingSetup = false;
  protected errorMessage = '';

  ngOnInit(): void {
    if (this.adminSession.requiresMfaSetup) {
      this.loadSetupChallenge();
    }
  }

  protected get requiresSetup(): boolean {
    return this.adminSession.requiresMfaSetup;
  }

  protected get requiresVerification(): boolean {
    return this.adminSession.requiresMfaVerification;
  }

  protected loadSetupChallenge(force = false): void {
    if (!this.requiresSetup || (this.setupChallenge && !force) || this.backupCodes.length > 0) {
      return;
    }
    this.isLoadingSetup = true;
    this.errorMessage = '';
    this.adminSession.beginMfaSetup().pipe(
      take(1),
      finalize(() => {
        this.isLoadingSetup = false;
      }),
    ).subscribe({
      next: (challenge) => {
        this.setupChallenge = challenge;
      },
      error: () => {
        this.errorMessage = 'Unable to prepare MFA setup right now. Please try again.';
      },
    });
  }

  protected confirmSetup(): void {
    if (!this.setupCode.trim()) {
      this.errorMessage = 'Enter the 6-digit code from your authenticator app to finish setup.';
      return;
    }
    this.isBusy = true;
    this.errorMessage = '';
    this.adminSession.confirmMfaSetup(this.setupCode.trim()).pipe(
      take(1),
      finalize(() => {
        this.isBusy = false;
      }),
    ).subscribe({
      next: (result) => {
        this.backupCodes = result.backupCodes;
        this.setupCode = '';
      },
      error: (error: unknown) => {
        this.errorMessage = this.resolveErrorMessage(error, 'The authenticator code was not accepted. Please try again.');
      },
    });
  }

  protected verifyMfa(): void {
    const code = this.useRecoveryCode ? null : this.loginCode.trim();
    const recoveryCode = this.useRecoveryCode ? this.recoveryCode.trim() : null;
    if (!code && !recoveryCode) {
      this.errorMessage = this.useRecoveryCode
        ? 'Enter one of your saved recovery codes.'
        : 'Enter the 6-digit code from your authenticator app.';
      return;
    }
    this.isBusy = true;
    this.errorMessage = '';
    this.adminSession.verifyMfa(code, recoveryCode).pipe(
      take(1),
      finalize(() => {
        this.isBusy = false;
      }),
    ).subscribe({
      next: async () => {
        this.loginCode = '';
        this.recoveryCode = '';
        await this.router.navigate(['/admin']);
      },
      error: (error: unknown) => {
        this.errorMessage = this.resolveErrorMessage(error, 'The MFA code was not accepted. Please try again.');
      },
    });
  }

  protected continueToCms(): void {
    void this.router.navigate(['/admin']);
  }

  protected signOut(): void {
    this.adminSession.logout(true);
  }

  private resolveErrorMessage(error: unknown, fallback: string): string {
    if (error instanceof HttpErrorResponse && typeof error.error?.detail === 'string' && error.error.detail.trim()) {
      return error.error.detail;
    }
    return fallback;
  }
}
