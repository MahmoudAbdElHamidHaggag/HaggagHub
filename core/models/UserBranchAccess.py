from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.session import Base

class UserBranchAccess(Base):
    __tablename__ = "user_branch_access"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # الصلاحية العامة
    is_all: Mapped[bool] = mapped_column(default=True) # إذا كانت True، هو يرى كل الفروع
    
    # الصلاحية المخصصة (تُفعل فقط إذا كانت is_all = False)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"), nullable=True)

    # علاقة للوصول السريع
    user = relationship("User", back_populates="branch_access")
    branch = relationship("Branch")