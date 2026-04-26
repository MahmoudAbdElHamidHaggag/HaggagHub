import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from database.base import Base


class AbstractBaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    is_synced: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    created_by: Mapped[str] = mapped_column(default="system")

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    updated_by: Mapped[str] = mapped_column(default="system")