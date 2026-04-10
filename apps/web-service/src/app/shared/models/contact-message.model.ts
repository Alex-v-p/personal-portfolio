export interface ContactMessageDraft {
  name: string;
  email: string;
  subject: string;
  message: string;
  sourcePage: string;
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
