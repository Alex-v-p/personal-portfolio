import { ResolvedMedia } from '../resolved-media.model';

export interface AdminMediaFile {
  id: string;
  bucketName: string;
  objectKey: string;
  originalFilename: string;
  mimeType?: string | null;
  visibility: string;
  altText?: string | null;
  title?: string | null;
  publicUrl?: string | null;
  resolvedAsset?: ResolvedMedia | null;
  createdAt: string;
  updatedAt: string;
}
