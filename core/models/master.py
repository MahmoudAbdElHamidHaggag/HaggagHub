from sqlalchemy.orm import Mapped, mapped_column
from .base import AbstractBaseModel # هذا هو الأب الذي صنعناه سابقاً

class MasterDataModel(AbstractBaseModel):
    __abstract__ = True
    
    code: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column()                       
    is_active: Mapped[bool] = mapped_column(default=True)     