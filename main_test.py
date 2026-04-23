from database.session import SessionLocal
from core.models.branch import Branch

def test_insert_branch():
    # 1. فتح جلسة اتصال بقاعدة البيانات
    db = SessionLocal()
    
    try:
        # 2. إنشاء كائن جديد من موديل الفرع
        new_branch = Branch(
            code="BR001", 
            name="الفرع الرئيسي", 
            address="بريدة، السعودية",
            is_active=True
        )
        
        # 3. حفظ البيانات
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        
        print(f"نجاح! تم إضافة الفرع بنجاح برقم تعريف (ID): {new_branch.id}")
        print(f"بيانات الفرع: {new_branch.name} - كود: {new_branch.code}")
        
    except Exception as e:
        print(f"حدث خطأ: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_insert_branch()