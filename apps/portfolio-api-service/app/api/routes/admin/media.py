from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, File, Form, Request, UploadFile, status

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.repository.media import AdminMediaRepository
from app.domains.admin.schema import AdminMediaFileOut, AdminMediaUploadOut
from app.domains.admin.service.media_management_service import AdminMediaManagementService

router = APIRouter()


@router.get('/media-files', response_model=list[AdminMediaFileOut])
def list_media_files(_: CurrentAdminDep, session: SessionDep) -> list[AdminMediaFileOut]:
    return AdminMediaRepository(session).list_media_files()


@router.post('/media-files/upload', response_model=AdminMediaUploadOut, status_code=status.HTTP_201_CREATED)
async def upload_media_file(
    request: Request,
    current_admin: CurrentAdminDep,
    session: SessionDep,
    file: UploadFile = File(...),
    folder: str | None = Form(default=None),
    title: str | None = Form(default=None),
    alt_text: str | None = Form(default=None, alias='altText'),
    description: str | None = Form(default=None),
    visibility: str = Form(default='public'),
) -> AdminMediaUploadOut:
    service = AdminMediaManagementService(session)
    service.validate_upload_request(request, admin_identifier=str(current_admin.id), visibility=visibility)
    return service.upload_bytes(
        file_bytes=await file.read(),
        original_filename=file.filename or 'upload',
        mime_type=file.content_type,
        folder=folder,
        title=title,
        alt_text=alt_text,
        description=description,
        visibility=visibility,
        uploaded_by_id=current_admin.id,
    )


@router.delete('/media-files/{media_id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_media_file(media_id: UUID, _: CurrentAdminDep, session: SessionDep) -> None:
    deleted = AdminMediaManagementService(session).delete_media(media_id)
    if not deleted:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail='Media file not found.')
