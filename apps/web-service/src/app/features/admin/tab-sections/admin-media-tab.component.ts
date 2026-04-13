import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { AdminDashboardSummary, AdminMediaFile } from '../../../shared/models/admin.model';
import { AdminMediaKind, isImageMedia, mediaFolder, mediaKindLabel } from '../admin-page.display.utils';

@Component({
  selector: 'app-admin-media-tab',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-media-tab.component.html'
})
export class AdminMediaTabComponent {
  @Input({ required: true }) dashboard!: AdminDashboardSummary;
  @Input({ required: true }) imageMediaCount = 0;
  @Input({ required: true }) documentMediaCount = 0;
  @Input({ required: true }) filteredMediaCount = 0;
  @Input({ required: true }) mediaSearchTerm = '';
  @Input({ required: true }) mediaVisibilityFilter: 'all' | 'public' | 'private' | 'signed' = 'all';
  @Input({ required: true }) mediaKindFilter: 'all' | AdminMediaKind = 'all';
  @Input({ required: true }) mediaFolderFilter = 'all';
  @Input({ required: true }) mediaFolderOptions: string[] = [];
  @Input({ required: true }) filteredMediaFiles: AdminMediaFile[] = [];
  @Input() selectedMediaFileId: string | null = null;
  @Input() selectedMediaFile: AdminMediaFile | null = null;
  @Input() deletingMediaFileIds: string[] = [];

  @Output() readonly mediaSearchTermChange = new EventEmitter<string>();
  @Output() readonly mediaVisibilityFilterChange = new EventEmitter<'all' | 'public' | 'private' | 'signed'>();
  @Output() readonly mediaKindFilterChange = new EventEmitter<'all' | AdminMediaKind>();
  @Output() readonly mediaFolderFilterChange = new EventEmitter<string>();
  @Output() readonly resetFilters = new EventEmitter<void>();
  @Output() readonly mediaSelected = new EventEmitter<string>();
  @Output() readonly deleteSelectedMedia = new EventEmitter<void>();

  onMediaSearchTermChange(value: string): void {
    this.mediaSearchTermChange.emit(value);
  }

  onMediaVisibilityFilterChange(value: 'all' | 'public' | 'private' | 'signed'): void {
    this.mediaVisibilityFilterChange.emit(value);
  }

  onMediaKindFilterChange(value: 'all' | AdminMediaKind): void {
    this.mediaKindFilterChange.emit(value);
  }

  onMediaFolderFilterChange(value: string): void {
    this.mediaFolderFilterChange.emit(value);
  }

  clearMediaFilters(): void {
    this.resetFilters.emit();
  }

  selectMediaFile(mediaId: string): void {
    this.mediaSelected.emit(mediaId);
  }

  deleteSelectedMediaFile(): void {
    this.deleteSelectedMedia.emit();
  }

  isDeletingMediaFile(mediaId: string): boolean {
    return this.deletingMediaFileIds.includes(mediaId);
  }

  isImageMedia(media: AdminMediaFile): boolean {
    return isImageMedia(media);
  }

  mediaFolder(media: AdminMediaFile): string {
    return media.folder || mediaFolder(media);
  }

  mediaKindLabel(media: AdminMediaFile): string {
    return mediaKindLabel(media);
  }

  formatFileSize(bytes: number | null | undefined): string {
    if (!bytes || bytes <= 0) {
      return 'Unknown size';
    }
    const units = ['B', 'KB', 'MB', 'GB'];
    let value = bytes;
    let unitIndex = 0;
    while (value >= 1024 && unitIndex < units.length - 1) {
      value /= 1024;
      unitIndex += 1;
    }
    const rounded = value >= 10 || unitIndex === 0 ? Math.round(value) : Number(value.toFixed(1));
    return `${rounded} ${units[unitIndex]}`;
  }

  usageItems(media: AdminMediaFile): Array<{ label: string; count: number }> {
    const usage = media.usageSummary;
    return [
      { label: 'Profile avatar', count: usage.profileAvatarCount },
      { label: 'Profile hero', count: usage.profileHeroCount },
      { label: 'Profile resume', count: usage.profileResumeCount },
      { label: 'Experience logos', count: usage.experienceLogoCount },
      { label: 'Project covers', count: usage.projectCoverCount },
      { label: 'Project gallery', count: usage.projectGalleryImageCount },
      { label: 'Blog covers', count: usage.blogCoverCount },
    ].filter((item) => item.count > 0);
  }
}
