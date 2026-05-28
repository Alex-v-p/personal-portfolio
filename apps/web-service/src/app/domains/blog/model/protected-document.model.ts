export interface ProtectedDocument {
  id: string;
  title: string;
  fileName?: string;
  mimeType?: string;
  fileSizeBytes?: number;
  downloadUrl: string;
}

export interface ProtectedDocumentGroup {
  slug: string;
  title: string;
  description?: string;
  documents: ProtectedDocument[];
}

export interface ProtectedDocumentsAccess {
  unlocked: boolean;
  expiresInSeconds: number;
}
