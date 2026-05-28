export interface ScopedUploadForm {
  title: string;
  altText: string;
  description: string;
  visibility: 'public' | 'private' | 'signed';
  file: File | null;
}

export function createEmptyScopedUploadForm(): ScopedUploadForm {
  return { title: '', altText: '', description: '', visibility: 'public', file: null };
}
