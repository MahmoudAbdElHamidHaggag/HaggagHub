from database.session import engine
from sqlalchemy import text

try:
    # محاولة فتح اتصال بسيط بقاعدة البيانات
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ تم الاتصال بقاعدة البيانات بنجاح!")
except Exception as e:
    print(f"❌ فشل الاتصال. السبب: {e}")