from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminExperienceOut, AdminExperiencesListOut, AdminExperienceUpsertIn
from app.domains.admin.service.admin_experience_service import AdminExperienceService

router = APIRouter()


@router.get('/experiences', response_model=AdminExperiencesListOut)
def list_experiences(_: CurrentAdminDep, session: SessionDep) -> AdminExperiencesListOut:
    return AdminExperienceService(session).list_experiences()


@router.get('/experiences/{experience_id}', response_model=AdminExperienceOut)
def get_experience(experience_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    return AdminExperienceService(session).get_experience(experience_id)


@router.post('/experiences', response_model=AdminExperienceOut, status_code=status.HTTP_201_CREATED)
def create_experience(payload: AdminExperienceUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    return AdminExperienceService(session).create_experience(payload)


@router.put('/experiences/{experience_id}', response_model=AdminExperienceOut)
def update_experience(experience_id: UUID, payload: AdminExperienceUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    return AdminExperienceService(session).update_experience(experience_id, payload)


@router.delete('/experiences/{experience_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_experience(experience_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminExperienceService(session).delete_experience(experience_id)
