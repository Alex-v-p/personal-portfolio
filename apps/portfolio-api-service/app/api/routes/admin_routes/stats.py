from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.routes.admin_routes.common import CurrentAdminDep, SessionDep
from app.repositories.admin.stats import AdminGithubRepository
from app.schemas.admin import (
    AdminGithubSnapshotOut,
    AdminGithubSnapshotRefreshIn,
    AdminGithubSnapshotsListOut,
    AdminGithubSnapshotUpsertIn,
)
from app.services.admin.github_snapshot_service import AdminGithubSnapshotService

router = APIRouter()


def repository(session: SessionDep) -> AdminGithubRepository:
    return AdminGithubRepository(session)


@router.get('/github-snapshots', response_model=AdminGithubSnapshotsListOut)
def list_github_snapshots(_: CurrentAdminDep, session: SessionDep) -> AdminGithubSnapshotsListOut:
    items = repository(session).list_github_snapshots()
    return AdminGithubSnapshotsListOut(items=items, total=len(items))


@router.get('/github-snapshots/{snapshot_id}', response_model=AdminGithubSnapshotOut)
def get_github_snapshot(snapshot_id: UUID, _: CurrentAdminDep, session: SessionDep) -> AdminGithubSnapshotOut:
    snapshot = repository(session).get_github_snapshot(snapshot_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')
    return snapshot


@router.post('/github-snapshots', response_model=AdminGithubSnapshotOut, status_code=status.HTTP_201_CREATED)
def create_github_snapshot(payload: AdminGithubSnapshotUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminGithubSnapshotOut:
    return repository(session).create_github_snapshot(payload)


@router.post('/github-snapshots/refresh', response_model=AdminGithubSnapshotOut)
def refresh_github_snapshot(payload: AdminGithubSnapshotRefreshIn, _: CurrentAdminDep, session: SessionDep) -> AdminGithubSnapshotOut:
    return AdminGithubSnapshotService(session).refresh(payload.username, prune_history=payload.prune_history)


@router.put('/github-snapshots/{snapshot_id}', response_model=AdminGithubSnapshotOut)
def update_github_snapshot(snapshot_id: UUID, payload: AdminGithubSnapshotUpsertIn, _: CurrentAdminDep, session: SessionDep) -> AdminGithubSnapshotOut:
    snapshot = repository(session).update_github_snapshot(snapshot_id, payload)
    if snapshot is None:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')
    return snapshot


@router.delete('/github-snapshots/{snapshot_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_github_snapshot(snapshot_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = repository(session).delete_github_snapshot(snapshot_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='GitHub snapshot not found.')
