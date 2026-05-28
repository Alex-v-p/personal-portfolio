from __future__ import annotations

from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class GithubSnapshot(Base):
    __tablename__ = 'github_snapshots'
    __table_args__ = (
        UniqueConstraint('snapshot_date', 'username', name='uq_github_snapshots_date_username'),
        CheckConstraint('public_repo_count >= 0', name='ck_github_snapshots_public_repo_count_nonnegative'),
        CheckConstraint('followers_count IS NULL OR followers_count >= 0', name='ck_github_snapshots_followers_nonnegative'),
        CheckConstraint('following_count IS NULL OR following_count >= 0', name='ck_github_snapshots_following_nonnegative'),
        CheckConstraint('total_stars IS NULL OR total_stars >= 0', name='ck_github_snapshots_total_stars_nonnegative'),
        CheckConstraint('total_commits IS NULL OR total_commits >= 0', name='ck_github_snapshots_total_commits_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    public_repo_count: Mapped[int] = mapped_column(Integer, nullable=False)
    followers_count: Mapped[int | None] = mapped_column(Integer)
    following_count: Mapped[int | None] = mapped_column(Integer)
    total_stars: Mapped[int | None] = mapped_column(Integer)
    total_commits: Mapped[int | None] = mapped_column(Integer)
    raw_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    contribution_days: Mapped[list['GithubContributionDay']] = relationship(
        back_populates='snapshot', cascade='all, delete-orphan'
    )


class GithubContributionDay(Base):
    __tablename__ = 'github_contribution_days'
    __table_args__ = (
        UniqueConstraint('snapshot_id', 'contribution_date', name='uq_github_contribution_days_snapshot_date'),
        CheckConstraint('contribution_count >= 0', name='ck_github_contribution_days_count_nonnegative'),
        CheckConstraint('level >= 0', name='ck_github_contribution_days_level_nonnegative'),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    snapshot_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey('github_snapshots.id', ondelete='CASCADE'), nullable=False
    )
    contribution_date: Mapped[date] = mapped_column(Date, nullable=False)
    contribution_count: Mapped[int] = mapped_column(Integer, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)

    snapshot: Mapped[GithubSnapshot] = relationship(back_populates='contribution_days')
