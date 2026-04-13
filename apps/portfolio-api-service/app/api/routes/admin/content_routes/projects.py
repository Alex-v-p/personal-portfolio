from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.api.routes.admin.content_routes.common import repository
from app.domains.admin.schema import AdminProjectOut, AdminProjectsListOut, AdminProjectUpsertIn

router = APIRouter()


@router.get('/projects', response_model=AdminProjectsListOut)
def list_projects(_: CurrentAdminDep, session: SessionDep) -> AdminProjectsListOut:
    items = repository(session).list_projects()
    return AdminProjectsListOut(items=items, total=len(items))


@router.get('/projects/{project_id}', response_model=AdminProjectOut)
def get_project(project_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    project = repository(session).get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.post('/projects', response_model=AdminProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: AdminProjectUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    return repository(session).create_project(payload)


@router.put('/projects/{project_id}', response_model=AdminProjectOut)
def update_project(project_id: UUID, payload: AdminProjectUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    project = repository(session).update_project(project_id, payload)
    if project is None:
        raise HTTPException(status_code=404, detail='Project not found.')
    return project


@router.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_project(project_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_project(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Project not found.')
