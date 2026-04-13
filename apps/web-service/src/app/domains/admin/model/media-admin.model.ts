import { ResolvedMedia } from '@domains/media/model/resolved-media.model';

export interface AdminMediaUsageSummary {
  profileAvatarCount: number;
  profileHeroCount: number;
  profileResumeCount: number;
  experienceLogoCount: number;
  projectCoverCount: number;
  projectGalleryImageCount: number;
  blogCoverCount: number;
  totalReferences: number;
  isReferenced: boolean;
}

export interface AdminMediaFile {
  id: string;
  bucketName: string;
  objectKey: string;
  originalFilename: string;
  storedFilename?: string | null;
  mimeType?: string | null;
  fileSizeBytes?: number | null;
  checksum?: string | null;
  description?: string | null;
  visibility: string;
  altText?: string | null;
  title?: string | null;
  publicUrl?: string | null;
  folder?: string | null;
  resolvedAsset?: ResolvedMedia | null;
  usageSummary: AdminMediaUsageSummary;
  canDelete: boolean;
  createdAt: string;
  updatedAt: string;
}
