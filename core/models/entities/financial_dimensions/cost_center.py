from sqlalchemy import String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base.abstract_base import AbstractBaseModel


class CostCenter(AbstractBaseModel):
    __tablename__ = "cost_centers"

    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey('tenants.id'), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    parent_id: Mapped[str] = mapped_column(String(36), ForeignKey('cost_centers.id'), nullable=True)
    manager_name: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey('branches.id'), nullable=True)
