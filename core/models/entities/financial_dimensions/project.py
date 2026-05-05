from sqlalchemy import String, Text, ForeignKey, Boolean, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from core.models.base.abstract_base import AbstractBaseModel


class ProjectStatus:
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Project(AbstractBaseModel):
    __tablename__ = "projects"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=ProjectStatus.PLANNING)
    start_date: Mapped[datetime] = mapped_column(nullable=True)
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    budget: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    actual_cost: Mapped[float] = mapped_column(Numeric(15, 4), default=0.0000)
    manager_name: Mapped[str] = mapped_column(String(100), nullable=True)
    customer_name: Mapped[str] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    cost_center_id: Mapped[str] = mapped_column(String(36), nullable=True)
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey('branches.id'), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
