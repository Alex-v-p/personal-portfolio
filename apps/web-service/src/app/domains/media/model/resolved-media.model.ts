export interface ResolvedMedia {
  id: string;
  url: string;
  downloadUrl?: string | null;
  alt?: string | null;
  fileName?: string | null;
  mimeType?: string | null;
  width?: number | null;
  height?: number | null;
}
