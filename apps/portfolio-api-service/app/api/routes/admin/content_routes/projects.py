from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema import AdminProjectOut, AdminProjectsListOut, AdminProjectUpsertIn
from app.domains.admin.service.admin_projects_service import AdminProjectsService

router = APIRouter()


@router.get('/projects', response_model=AdminProjectsListOut)
def list_projects(_: CurrentAdminDep, session: SessionDep) -> AdminProjectsListOut:
    return AdminProjectsService(session).list_projects()


@router.get('/projects/{project_id}', response_model=AdminProjectOut)
def get_project(project_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    return AdminProjectsService(session).get_project(project_id)


@router.post('/projects', response_model=AdminProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: AdminProjectUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    return AdminProjectsService(session).create_project(payload)


@router.put('/projects/{project_id}', response_model=AdminProjectOut)
def update_project(project_id: UUID, payload: AdminProjectUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminProjectOut:
    return AdminProjectsService(session).update_project(project_id, payload)


@router.delete('/projects/{project_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_project(project_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    AdminProjectsService(session).delete_project(project_id)
