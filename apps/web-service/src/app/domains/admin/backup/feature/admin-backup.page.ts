import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { take } from 'rxjs/operators';

import { AdminBackupApiService } from '@domains/admin/data/api/admin-backup-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminBackupImportResult } from '@domains/admin/model/backup-admin.model';

@Component({
  selector: 'app-admin-backup-page',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-backup.page.html',
})
export class AdminBackupPageComponent {
  private readonly backupApi = inject(AdminBackupApiService);
  private readonly adminSession = inject(AdminSessionService);

  protected selectedFile: File | null = null;
  protected replaceExisting = true;
  protected isExporting = false;
  protected isImporting = false;
  protected statusMessage = '';
  protected errorMessage = '';
  protected importResult: AdminBackupImportResult | null = null;

  protected readonly exportedSections = [
    'Profile, social links, and navigation',
    'Skills, skill categories, projects, galleries, and experience',
    'Blog posts, topics, GitHub snapshots, and contact messages',
    'Assistant-only context notes',
    'Media metadata plus uploaded media files/images inside the backup zip',
  ];

  protected exportBackup(): void {
    this.isExporting = true;
    this.statusMessage = 'Preparing CSV backup…';
    this.errorMessage = '';

    this.backupApi.exportBackup().pipe(take(1)).subscribe({
      next: (blob) => {
        this.downloadBlob(blob);
        this.statusMessage = 'Backup exported with CSV data and available media files. Keep it somewhere safe.';
        this.isExporting = false;
      },
      error: (error) => this.handleError(error, 'Exporting the CMS backup failed.'),
    });
  }

  protected onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement | null;
    this.selectedFile = input?.files?.[0] ?? null;
    this.importResult = null;
    this.errorMessage = '';
  }

  protected importBackup(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Choose a CMS backup .zip file first.';
      return;
    }

    const confirmed = window.confirm(
      this.replaceExisting
        ? 'This will replace the current CMS content with the selected backup. Admin users are not changed. Continue?'
        : 'This will import records from the backup without clearing existing content first. Duplicate IDs may fail. Continue?',
    );
    if (!confirmed) {
      return;
    }

    this.isImporting = true;
    this.statusMessage = 'Importing CMS backup…';
    this.errorMessage = '';
    this.importResult = null;

    this.backupApi.importBackup(this.selectedFile, this.replaceExisting).pipe(take(1)).subscribe({
      next: (result) => {
        this.importResult = result;
        this.statusMessage = 'Backup imported. Rebuild assistant knowledge and restore/re-upload media files if object storage was wiped.';
        this.isImporting = false;
      },
      error: (error) => this.handleError(error, 'Importing the CMS backup failed.'),
    });
  }

  protected importedEntries(): Array<{ file: string; count: number }> {
    if (!this.importResult) {
      return [];
    }
    return Object.entries(this.importResult.imported)
      .map(([file, count]) => ({ file, count }))
      .sort((a, b) => a.file.localeCompare(b.file));
  }

  private handleError(error: any, fallback: string): void {
    if (error?.status === 401) {
      this.adminSession.logout();
      return;
    }

    this.isExporting = false;
    this.isImporting = false;
    this.statusMessage = '';
    this.errorMessage = error?.error?.detail || fallback;
  }

  private downloadBlob(blob: Blob): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    link.href = url;
    link.download = `portfolio-cms-backup-${timestamp}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}
