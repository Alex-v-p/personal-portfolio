from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.api.routes.admin.content_routes.common import repository
from app.domains.admin.schema import AdminExperienceOut, AdminExperiencesListOut, AdminExperienceUpsertIn

router = APIRouter()


@router.get('/experiences', response_model=AdminExperiencesListOut)
def list_experiences(_: CurrentAdminDep, session: SessionDep) -> AdminExperiencesListOut:
    items = repository(session).list_experiences()
    return AdminExperiencesListOut(items=items, total=len(items))


@router.get('/experiences/{experience_id}', response_model=AdminExperienceOut)
def get_experience(experience_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    experience = repository(session).get_experience(experience_id)
    if experience is None:
        raise HTTPException(status_code=404, detail='Experience entry not found.')
    return experience


@router.post('/experiences', response_model=AdminExperienceOut, status_code=status.HTTP_201_CREATED)
def create_experience(payload: AdminExperienceUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    return repository(session).create_experience(payload)


@router.put('/experiences/{experience_id}', response_model=AdminExperienceOut)
def update_experience(experience_id: UUID, payload: AdminExperienceUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminExperienceOut:
    experience = repository(session).update_experience(experience_id, payload)
    if experience is None:
        raise HTTPException(status_code=404, detail='Experience entry not found.')
    return experience


@router.delete('/experiences/{experience_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_experience(experience_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_experience(experience_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Experience entry not found.')
