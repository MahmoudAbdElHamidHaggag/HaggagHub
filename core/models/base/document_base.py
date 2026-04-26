from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import AbstractBaseModel


class DocumentBaseModel(AbstractBaseModel):
    __abstract__ = True

    company_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("companies.id"),
        index=True
    )

    branch_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("branches.id"),
        index=True
    )

    cost_center_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("cost_centers.id"),
        index=True
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id"),
        index=True
    )

    notes: Mapped[str] = mapped_column(nullable=True)

    # relationships
    company = relationship("Company")
    branch = relationship("Branch")
    cost_center = relationship("CostCenter")
    user = relationship("User")