from __future__ import annotations

from fastapi import APIRouter, Request, Response, status

from app.api.routes.admin.common import CurrentAdminSessionDep, SessionDep
from app.domains.admin.schema import (
    AdminAuthSessionOut,
    AdminLoginIn,
    AdminMfaSetupConfirmIn,
    AdminMfaSetupConfirmOut,
    AdminMfaSetupStartOut,
    AdminMfaVerifyIn,
)
from app.domains.admin.service.auth_service import AdminAuthService

router = APIRouter()


@router.post('/auth/login', response_model=AdminAuthSessionOut)
def login(payload: AdminLoginIn, request: Request, response: Response, session: SessionDep) -> AdminAuthSessionOut:
    return AdminAuthService(session).login(payload, request=request, response=response)


@router.get('/auth/me', response_model=AdminAuthSessionOut)
def get_me(current_session: CurrentAdminSessionDep, session: SessionDep) -> AdminAuthSessionOut:
    return AdminAuthService(session).build_authenticated_session(current_session)


@router.post('/auth/mfa/setup', response_model=AdminMfaSetupStartOut)
def begin_mfa_setup(current_session: CurrentAdminSessionDep, request: Request, session: SessionDep) -> AdminMfaSetupStartOut:
    return AdminAuthService(session).begin_mfa_setup(current_session, request=request)


@router.post('/auth/mfa/setup/confirm', response_model=AdminMfaSetupConfirmOut)
def confirm_mfa_setup(
    payload: AdminMfaSetupConfirmIn,
    current_session: CurrentAdminSessionDep,
    request: Request,
    session: SessionDep,
) -> AdminMfaSetupConfirmOut:
    return AdminAuthService(session).confirm_mfa_setup(current_session, payload, request=request)


@router.post('/auth/mfa/verify', response_model=AdminAuthSessionOut)
def verify_mfa(
    payload: AdminMfaVerifyIn,
    current_session: CurrentAdminSessionDep,
    request: Request,
    session: SessionDep,
) -> AdminAuthSessionOut:
    return AdminAuthService(session).verify_mfa(current_session, payload, request=request)


@router.post('/auth/logout', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def logout(current_session: CurrentAdminSessionDep, request: Request, response: Response, session: SessionDep) -> None:
    AdminAuthService(session).logout(current_session, request=request, response=response)
