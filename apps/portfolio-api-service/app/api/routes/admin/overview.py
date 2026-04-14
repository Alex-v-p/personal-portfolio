from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.admin.common import CurrentAdminDep, SessionDep
from app.domains.admin.repository.overview import AdminOverviewRepository
from app.domains.admin.schema import AdminDashboardSummaryOut, AdminReferenceDataOut

router = APIRouter()


@router.get('/dashboard', response_model=AdminDashboardSummaryOut)
def get_dashboard_summary(_: CurrentAdminDep, session: SessionDep) -> AdminDashboardSummaryOut:
    return AdminOverviewRepository(session).get_dashboard_summary()


@router.get('/reference-data', response_model=AdminReferenceDataOut)
def get_reference_data(_: CurrentAdminDep, session: SessionDep) -> AdminReferenceDataOut:
    return AdminOverviewRepository(session).get_reference_data()
