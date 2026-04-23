# core/services/security_service.py
from sqlalchemy.orm import Session
from core.models.user import User
from core.models.branch import Branch
from core.models.UserBranchAccess import UserBranchAccess # افترض أنك وضعت الموديل هنا

def can_user_access_branch(db: Session, user_id: int, branch_id: int) -> bool:
    """
    تتحقق ما إذا كان المستخدم يملك صلاحية الوصول للفرع المطلوب
    """
    # 1. جلب سجل الصلاحية للمستخدم والفرع
    access = db.query(UserBranchAccess).filter(
        UserBranchAccess.user_id == user_id,
        UserBranchAccess.branch_id == branch_id
    ).first()
    
    # 2. إذا وجد السجل، فهو يملك صلاحية
    if access:
        return True
        
    # 3. المنطق الاحتياطي: هل يملك صلاحية "الكل"؟ (يمكنك إضافة حقل is_all في جدول المستخدم أو الصلاحيات)
    return False

def get_allowed_branches(db: Session, user_id: int):
    """
    ترجع قائمة بجميع الفروع المسموح للمستخدم برؤيتها
    """
    return db.query(Branch).join(UserBranchAccess).filter(
        UserBranchAccess.user_id == user_id
    ).all()