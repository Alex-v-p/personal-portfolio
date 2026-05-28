from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import AdminSession, AdminUser
from app.db.session import get_session
from app.services.security import get_current_admin_session, get_current_admin_user, require_admin_csrf, require_admin_mfa

SessionDep = Annotated[Session, Depends(get_session)]
CurrentAdminDep = Annotated[AdminUser, Depends(require_admin_mfa)]
CurrentAdminSessionDep = Annotated[AdminSession, Depends(get_current_admin_session)]
CurrentAuthenticatedAdminDep = Annotated[AdminUser, Depends(get_current_admin_user)]
AdminWriteProtectionDep = Annotated[None, Depends(require_admin_csrf)]


def not_found(detail: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
