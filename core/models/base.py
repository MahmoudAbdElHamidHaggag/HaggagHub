import uuid
from sqlalchemy import UUID 
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from database.session import Base 

class AbstractBaseModel(Base):
    __abstract__ = True
    
    __mapper_args__ = {"polymorphic_abstract": True}
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        default=uuid.uuid4  
    )
    
    is_synced: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), 
    )
    created_by: Mapped[str] = mapped_column(default="system")
    
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )
    updated_by: Mapped[str] = mapped_column(default="system")