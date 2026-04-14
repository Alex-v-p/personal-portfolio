from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import Boolean, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class NavigationItem(Base):
    __tablename__ = 'navigation_items'

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    route_path: Mapped[str] = mapped_column(String(255), nullable=False)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
