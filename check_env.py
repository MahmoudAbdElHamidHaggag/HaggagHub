from config import settings

def check_settings():
    print("--- اختبار تحميل الإعدادات ---")
    print(f"وضع التشغيل الحالي (App Mode): {settings.APP_MODE}")
    print(f"الرابط المستخدم حالياً (Active URL): {settings.DATABASE_URL}")
    
    if "postgresql" in settings.DATABASE_URL:
        print("✅ النظام جاهز للعمل بنمط السيرفر المركزي (Postgres).")
    elif "sqlite" in settings.DATABASE_URL:
        print("✅ النظام يعمل بنمط محلي (SQLite).")
    else:
        print("⚠️ الرابط غير معروف، راجع ملف .env")

if __name__ == "__main__":
    check_settings()