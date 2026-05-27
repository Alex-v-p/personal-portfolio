import { NgFor, NgIf } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { ChangeDetectorRef, Component, DestroyRef, Input, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs/operators';

import { TranslatePipe } from '@core/i18n/translate.pipe';
import { PublicBlogApiService } from '@domains/blog/data/blog-api.service';
import { ProtectedDocument, ProtectedDocumentGroup } from '@domains/blog/model/protected-document.model';
import { UiButtonComponent } from '@shared/components/button/ui-button.component';
import { UiIconComponent } from '@shared/icons';

@Component({
  selector: 'app-protected-documents-card',
  standalone: true,
  imports: [NgFor, NgIf, FormsModule, TranslatePipe, UiButtonComponent, UiIconComponent],
  templateUrl: './protected-documents-card.component.html',
})
export class ProtectedDocumentsCardComponent implements OnInit {
  private readonly blogApi = inject(PublicBlogApiService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);
  private readonly destroyRef = inject(DestroyRef);

  @Input({ required: true }) group!: ProtectedDocumentGroup;

  protected password = '';
  protected unlocked = false;
  protected isCheckingAccess = false;
  protected isUnlocking = false;
  protected errorMessage = '';

  ngOnInit(): void {
    if (!this.group?.slug) {
      return;
    }

    this.isCheckingAccess = true;
    this.blogApi
      .getProtectedDocumentAccess(this.group.slug)
      .pipe(
        finalize(() => {
          this.isCheckingAccess = false;
          this.changeDetectorRef.detectChanges();
        }),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (access) => {
          this.unlocked = access.unlocked;
        },
        error: () => {
          this.unlocked = false;
        },
      });
  }

  protected unlock(): void {
    if (!this.group?.slug || this.isUnlocking) {
      return;
    }

    this.errorMessage = '';
    const password = this.password.trim();
    if (!password) {
      this.errorMessage = 'pages.blogPost.protectedDocuments.errors.passwordRequired';
      return;
    }

    this.isUnlocking = true;
    this.blogApi
      .unlockProtectedDocuments(this.group.slug, password)
      .pipe(
        finalize(() => {
          this.isUnlocking = false;
          this.changeDetectorRef.detectChanges();
        }),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe({
        next: (access) => {
          this.unlocked = access.unlocked;
          this.password = '';
        },
        error: (error: HttpErrorResponse) => {
          this.errorMessage = this.mapUnlockError(error);
        },
      });
  }

  protected formatFileSize(document: ProtectedDocument): string {
    const bytes = document.fileSizeBytes;
    if (typeof bytes !== 'number' || bytes <= 0) {
      return document.mimeType ?? '';
    }

    if (bytes < 1024) {
      return `${bytes} B`;
    }

    const units = ['KB', 'MB', 'GB'];
    let value = bytes / 1024;
    for (const unit of units) {
      if (value < 1024 || unit === units[units.length - 1]) {
        return `${value.toFixed(value >= 10 ? 0 : 1)} ${unit}`;
      }
      value /= 1024;
    }

    return '';
  }

  private mapUnlockError(error: HttpErrorResponse): string {
    if (error.status === 401) {
      return 'pages.blogPost.protectedDocuments.errors.invalidPassword';
    }

    if (error.status === 429) {
      return 'pages.blogPost.protectedDocuments.errors.rateLimited';
    }

    if (error.status === 503) {
      return 'pages.blogPost.protectedDocuments.errors.notConfigured';
    }

    return 'pages.blogPost.protectedDocuments.errors.unlockFailed';
  }
}
