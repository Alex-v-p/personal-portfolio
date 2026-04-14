from __future__ import annotations

from pydantic import EmailStr, Field, model_validator

from app.schemas.base import ApiSchema


class AdminUserOut(ApiSchema):
    id: str
    email: str
    display_name: str
    is_active: bool
    created_at: str
    mfa_enabled: bool = False
    mfa_enrolled_at: str | None = None
    mfa_recovery_codes_remaining: int = 0


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


class AdminAuthSessionOut(ApiSchema):
    csrf_token: str
    expires_in_seconds: int
    user: AdminUserOut
    is_mfa_enabled: bool = False
    is_mfa_verified: bool = False
    mfa_required: bool = False
    mfa_setup_required: bool = False


class AdminLoginIn(ApiSchema):
    email: EmailStr
    password: str


class AdminMfaSetupStartOut(ApiSchema):
    manual_entry_key: str
    otpauth_uri: str
    qr_code_data_url: str
    issuer: str


class AdminMfaSetupConfirmIn(ApiSchema):
    code: str = Field(min_length=6, max_length=16)


class AdminMfaSetupConfirmOut(ApiSchema):
    backup_codes: list[str]
    session: AdminAuthSessionOut


class AdminMfaVerifyIn(ApiSchema):
    code: str | None = Field(default=None, min_length=6, max_length=16)
    recovery_code: str | None = Field(default=None, min_length=6, max_length=64)

    @model_validator(mode='after')
    def validate_code_or_recovery_code(self) -> 'AdminMfaVerifyIn':
        has_code = bool((self.code or '').strip())
        has_recovery = bool((self.recovery_code or '').strip())
        if has_code == has_recovery:
            raise ValueError('Provide exactly one of code or recoveryCode.')
        return self


__all__ = [
    'AdminAuthSessionOut',
    'AdminLoginIn',
    'AdminMfaSetupConfirmIn',
    'AdminMfaSetupConfirmOut',
    'AdminMfaSetupStartOut',
    'AdminMfaVerifyIn',
    'AdminUserCreateIn',
    'AdminUserOut',
    'AdminUserUpdateIn',
]
