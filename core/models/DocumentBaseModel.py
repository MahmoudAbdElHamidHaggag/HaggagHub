import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import AbstractBaseModel

class DocumentBaseModel(AbstractBaseModel):
    __abstract__ = True
    
    branch_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("branches.id"), index=True)
    cost_center_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("cost_centers.id"), index=True)
    
    notes: Mapped[str] = mapped_column(default="", nullable=True)