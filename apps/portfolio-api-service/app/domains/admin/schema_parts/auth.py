from __future__ import annotations

from pydantic import EmailStr, Field

from app.schemas.base import ApiSchema


class AdminUserOut(ApiSchema):
    id: str
    email: str
    display_name: str
    is_active: bool
    created_at: str


class AdminUserCreateIn(ApiSchema):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=8, max_length=255)
    is_active: bool = True


class AdminUserUpdateIn(ApiSchema):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=120)
    password: str | None = Field(default=None, min_length=8, max_length=255)
    is_active: bool = True


class AdminAuthTokenOut(ApiSchema):
    access_token: str
    token_type: str = 'bearer'
    expires_in_seconds: int
    user: AdminUserOut


class AdminLoginIn(ApiSchema):
    email: EmailStr
    password: str


__all__ = [
    'AdminAuthTokenOut',
    'AdminLoginIn',
    'AdminUserCreateIn',
    'AdminUserOut',
    'AdminUserUpdateIn',
]
