from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.schema_parts.backup import AdminBackupImportOut
from app.domains.admin.service.admin_backup_service import AdminBackupService

router = APIRouter()


@router.get('/backup/export')
def export_cms_backup(_: CurrentAdminDep, session: SessionDep) -> Response:
    archive_bytes = AdminBackupService(session).export_csv_zip()
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')
    return Response(
        content=archive_bytes,
        media_type='application/zip',
        headers={'Content-Disposition': f'attachment; filename="portfolio-cms-backup-{timestamp}.zip"'},
    )


@router.post('/backup/import', response_model=AdminBackupImportOut)
async def import_cms_backup(
    _: CurrentAdminDep,
    session: SessionDep,
    file: UploadFile = File(...),
    replace_existing: bool = Form(default=True, alias='replaceExisting'),
) -> AdminBackupImportOut:
    if not file.filename or not file.filename.lower().endswith('.zip'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please upload a CMS backup .zip file.')

    try:
        result = AdminBackupService(session).import_csv_zip(await file.read(), replace_existing=replace_existing)
        session.commit()
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return AdminBackupImportOut(**result)
