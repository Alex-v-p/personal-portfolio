import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';
import { forkJoin } from 'rxjs';
import { finalize, take } from 'rxjs/operators';

import { AdminMediaApiService } from '@domains/admin/data/api/admin-media-api.service';
import { AdminOverviewApiService } from '@domains/admin/data/api/admin-overview-api.service';
import { AdminSessionService } from '@domains/admin/data/admin-session.service';
import { AdminDashboardSummary, AdminMediaFile } from '@domains/admin/model/admin.model';
import { AdminMediaTabComponent } from '@domains/admin/ui/tabs/admin-media-tab.component';
import {
  MediaKindFilter,
  MediaVisibilityFilter,
  buildMediaFolderOptions,
  countMediaByKind,
  filterMediaFiles,
  resolveSelectedMediaFile,
} from '@domains/admin/media/state/admin-media.filters';
import { resolveSelection } from '@domains/admin/shell/state/admin-page.utils';

@Component({
  selector: 'app-admin-media-page',
  standalone: true,
  imports: [CommonModule, AdminMediaTabComponent],
  templateUrl: './admin-media.page.html',
})
export class AdminMediaPageComponent implements OnInit {
  private readonly overviewApi = inject(AdminOverviewApiService);
  private readonly mediaApi = inject(AdminMediaApiService);
  private readonly adminSession = inject(AdminSessionService);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected isLoading = true;
  protected errorMessage = '';
  protected statusMessage = '';

  protected dashboard: AdminDashboardSummary = {
    projects: 0,
    blogPosts: 0,
    unreadMessages: 0,
    skills: 0,
    skillCategories: 0,
    mediaFiles: 0,
    experiences: 0,
    navigationItems: 0,
    blogTags: 0,
    adminUsers: 0,
    githubSnapshots: 0,
  };
  protected mediaFiles: AdminMediaFile[] = [];
  protected selectedMediaFileId: string | null = null;
  protected deletingMediaFileIds: string[] = [];

  protected mediaSearchTerm = '';
  protected mediaVisibilityFilter: MediaVisibilityFilter = 'all';
  protected mediaKindFilter: MediaKindFilter = 'all';
  protected mediaFolderFilter = 'all';

  ngOnInit(): void {
    this.loadMediaPage(false);
  }

  protected reload(): void {
    this.loadMediaPage(true);
  }

  protected get mediaFolderOptions(): string[] {
    return buildMediaFolderOptions(this.mediaFiles);
  }

  protected get filteredMediaFiles(): AdminMediaFile[] {
    return filterMediaFiles(this.mediaFiles, {
      searchTerm: this.mediaSearchTerm,
      visibility: this.mediaVisibilityFilter,
      kind: this.mediaKindFilter,
      folder: this.mediaFolderFilter,
    });
  }

  protected get filteredMediaCount(): number {
    return this.filteredMediaFiles.length;
  }

  protected get imageMediaCount(): number {
    return countMediaByKind(this.mediaFiles, 'image');
  }

  protected get documentMediaCount(): number {
    return countMediaByKind(this.mediaFiles, 'document');
  }

  protected get selectedMediaFile(): AdminMediaFile | null {
    return resolveSelectedMediaFile(this.mediaFiles, this.selectedMediaFileId);
  }

  protected clearMediaFilters(): void {
    this.mediaSearchTerm = '';
    this.mediaVisibilityFilter = 'all';
    this.mediaKindFilter = 'all';
    this.mediaFolderFilter = 'all';
  }

  protected selectMediaFile(mediaId: string): void {
    this.selectedMediaFileId = mediaId;
    this.statusMessage = '';
  }

  protected deleteSelectedMediaFile(): void {
    const media = this.selectedMediaFile;
    if (!media) {
      return;
    }
    if (!media.canDelete) {
      this.statusMessage = 'This media file is still referenced by portfolio content. Remove those references before deleting it.';
      return;
    }

    const confirmed = window.confirm(
      `Delete "${media.title || media.originalFilename}"? This removes the media record from the CMS and attempts to delete the stored file too.`,
    );
    if (!confirmed) {
      return;
    }

    this.deletingMediaFileIds = [...this.deletingMediaFileIds, media.id];
    this.statusMessage = 'Deleting media file…';
    this.mediaApi.deleteMediaFile(media.id).pipe(take(1)).subscribe({
      next: () => {
        this.selectedMediaFileId = null;
        this.deletingMediaFileIds = this.deletingMediaFileIds.filter((id) => id !== media.id);
        this.statusMessage = 'Media file deleted.';
        this.loadMediaPage(false);
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.deletingMediaFileIds = this.deletingMediaFileIds.filter((id) => id !== media.id);
        this.statusMessage = error?.error?.detail || 'Deleting the media file failed.';
        this.changeDetectorRef.detectChanges();
      },
    });
  }

  private loadMediaPage(showReloadMessage: boolean): void {
    const currentSelection = this.selectedMediaFileId;
    this.isLoading = true;
    this.errorMessage = '';
    if (showReloadMessage) {
      this.statusMessage = 'Refreshing media library…';
    }

    forkJoin({
      dashboard: this.overviewApi.getDashboardSummary(),
      mediaFiles: this.mediaApi.listMediaFiles(),
    }).pipe(
      take(1),
      finalize(() => {
        this.isLoading = false;
        this.changeDetectorRef.detectChanges();
      }),
    ).subscribe({
      next: ({ dashboard, mediaFiles }) => {
        this.dashboard = dashboard;
        this.mediaFiles = mediaFiles;
        if (this.mediaFolderFilter !== 'all' && !this.mediaFolderOptions.includes(this.mediaFolderFilter)) {
          this.mediaFolderFilter = 'all';
        }
        this.selectedMediaFileId = resolveSelection(currentSelection, this.filteredMediaFiles) ?? resolveSelection(currentSelection, this.mediaFiles);

        if (showReloadMessage) {
          this.statusMessage = 'Media library refreshed.';
        }
      },
      error: (error) => {
        if (error?.status === 401) {
          this.adminSession.logout();
          return;
        }

        this.errorMessage = error?.error?.detail || 'The media library could not be loaded.';
      },
    });
  }
}
