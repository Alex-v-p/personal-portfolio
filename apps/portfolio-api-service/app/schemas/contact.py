from __future__ import annotations

from pydantic import EmailStr, Field

from app.schemas.base import ApiSchema


class ContactMessageIn(ApiSchema):
    name: str = Field(min_length=2)
    email: EmailStr
    subject: str = Field(min_length=4, max_length=120)
    message: str = Field(min_length=20, max_length=1200)
    source_page: str = '/contact'


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
