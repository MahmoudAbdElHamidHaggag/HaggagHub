from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import AbstractBaseModel

class MasterDataModel(AbstractBaseModel):
    __abstract__ = True
    
    code: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()                       
    is_active: Mapped[bool] = mapped_column(default=True)     