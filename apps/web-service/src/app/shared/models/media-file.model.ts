export type FileVisibility = 'private' | 'public' | 'signed';

export interface MediaFile {
  id: string;
  bucketName: string;
  objectKey: string;
  originalFilename: string;
  storedFilename: string;
  mimeType: string;
  fileSizeBytes: number;
  checksum: string;
  publicUrl?: string;
  altText?: string;
  title?: string;
  description?: string;
  visibility: FileVisibility;
  uploadedBy?: string | null;
  createdAt: string;
  updatedAt: string;
}
