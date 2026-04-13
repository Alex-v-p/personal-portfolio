export type FileVisibility = 'private' | 'public' | 'signed';

export interface MediaFile {
  id: string;
  bucketName: string;
  objectKey: string;
  originalFilename: string;
  storedFilename?: string | null;
  mimeType?: string | null;
  fileSizeBytes?: number | null;
  checksum?: string | null;
  publicUrl?: string | null;
  altText?: string | null;
  title?: string | null;
  description?: string | null;
  folder?: string | null;
  visibility: FileVisibility;
  uploadedBy?: string | null;
  createdAt: string;
  updatedAt: string;
}
