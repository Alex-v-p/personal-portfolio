export interface ContactMessageDraft {
  name: string;
  email: string;
  subject: string;
  message: string;
  sourcePage: string;
  visitorId?: string | null;
  sessionId?: string | null;
  website?: string | null;
}

export interface ContactMessageRecord extends ContactMessageDraft {
  id: string;
  isRead: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ContactMessageCreatedResponse {
  message: string;
  item: ContactMessageRecord;
}
