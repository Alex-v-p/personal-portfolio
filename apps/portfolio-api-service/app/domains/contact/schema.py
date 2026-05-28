from __future__ import annotations

from pydantic import EmailStr, Field

from app.schemas.base import ApiSchema


class ContactMessageIn(ApiSchema):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    subject: str = Field(min_length=4, max_length=120)
    message: str = Field(min_length=20, max_length=1200)
    source_page: str = Field(default='/contact', max_length=255)
    visitor_id: str | None = Field(default=None, max_length=255)
    session_id: str | None = Field(default=None, max_length=255)
    website: str | None = Field(default=None, max_length=120)


class ContactMessageOut(ApiSchema):
    id: str
    name: str
    email: EmailStr
    subject: str
    message: str
    source_page: str
    is_read: bool
    created_at: str
    updated_at: str


class ContactMessageCreatedOut(ApiSchema):
    message: str
    item: ContactMessageOut
