export interface AdminBackupImportResult {
  imported: Record<string, number>;
  skippedFiles: string[];
  replaceExisting: boolean;
  warnings: string[];
}
