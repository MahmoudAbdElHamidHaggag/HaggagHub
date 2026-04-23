from sqlalchemy.orm import Mapped, mapped_column
from .master import MasterDataModel

class Branch(MasterDataModel):
    __tablename__ = "branches"  # اسم الجدول في قاعدة البيانات
    
    # حقول خاصة بالفرع فقط (الوراثة وفرت لنا id, code, name, is_active, etc.)
    address: Mapped[str] = mapped_column(default="", nullable=True)
    phone: Mapped[str] = mapped_column(default="", nullable=True)