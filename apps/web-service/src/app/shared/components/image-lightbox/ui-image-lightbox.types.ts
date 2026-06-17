export type UiImageLightboxItemType = 'image' | 'document';

export interface UiImageLightboxImage {
  id?: number | string | null;
  url: string;
  alt?: string | null;
  type?: UiImageLightboxItemType;
}
