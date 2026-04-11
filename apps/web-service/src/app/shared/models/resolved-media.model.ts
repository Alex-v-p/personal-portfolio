export interface ResolvedMedia {
  id: string;
  url: string;
  alt?: string | null;
  fileName?: string | null;
  mimeType?: string | null;
  width?: number | null;
  height?: number | null;
}
