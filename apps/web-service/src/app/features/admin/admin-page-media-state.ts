import { AdminMediaFile } from '../../shared/models/admin.model';
import { AdminMediaKind, mediaFolder, mediaKind } from './admin-page.display.utils';
import { ScopedUploadForm } from './admin-page.forms';
import { matchesSearch, slugify } from './admin-page.utils';

export type MediaVisibilityFilter = 'all' | 'public' | 'private' | 'signed';
export type MediaKindFilter = 'all' | AdminMediaKind;

export interface AdminMediaFilterState {
  searchTerm: string;
  visibility: MediaVisibilityFilter;
  kind: MediaKindFilter;
  folder: string;
}

export function buildMediaFolderOptions(mediaFiles: AdminMediaFile[]): string[] {
  return Array.from(new Set(mediaFiles.map((media) => mediaFolder(media)).filter((value) => value && value !== 'root'))).sort((left, right) => left.localeCompare(right));
}

export function filterMediaFiles(mediaFiles: AdminMediaFile[], filters: AdminMediaFilterState): AdminMediaFile[] {
  return mediaFiles
    .filter((media) => filters.visibility === 'all' || media.visibility === filters.visibility)
    .filter((media) => filters.kind === 'all' || mediaKind(media) === filters.kind)
    .filter((media) => filters.folder === 'all' || mediaFolder(media) === filters.folder)
    .filter((media) => matchesSearch([media.title, media.altText, media.originalFilename, media.objectKey, mediaFolder(media)], filters.searchTerm))
    .sort((left, right) => right.createdAt.localeCompare(left.createdAt));
}

export function countMediaByKind(mediaFiles: AdminMediaFile[], kind: AdminMediaKind): number {
  return mediaFiles.filter((media) => mediaKind(media) === kind).length;
}

export function resolveSelectedMediaFile(mediaFiles: AdminMediaFile[], selectedMediaFileId: string | null): AdminMediaFile | null {
  return mediaFiles.find((media) => media.id === selectedMediaFileId) ?? null;
}

export function buildProjectMediaFolder(slugOrTitle: string): string {
  return `projects/${slugify(slugOrTitle || 'untitled-project')}`;
}

export function buildBlogMediaFolder(slugOrTitle: string): string {
  return `blog/${slugify(slugOrTitle || 'untitled-post')}`;
}

export function buildProfileMediaFolder(firstName: string, lastName: string): string {
  const profileSlug = slugify(`${firstName || 'profile'}-${lastName || 'owner'}`);
  return `profiles/${profileSlug}`;
}

export function buildExperienceMediaFolder(organizationName: string, roleTitle: string): string {
  return `experience/${slugify(organizationName || roleTitle || 'experience')}`;
}

export function resetScopedUploadForm(form: ScopedUploadForm): void {
  form.title = '';
  form.altText = '';
  form.description = '';
  form.visibility = 'public';
  form.file = null;
}
