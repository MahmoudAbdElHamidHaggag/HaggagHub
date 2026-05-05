# HaggagHub ERP System

نظام ERP متعدد المستأجرين يعمل أونلاين وأوفلاين مع نظام اشتراكات مرن.

## المميزات الرئيسية

### 🏢 نظام متعدد المستأجرين (Multi-tenant)
- كل مستأجر يمثل شركة منفصلة
- عزل تام بين بيانات الشركات المختلفة
- دعم فروع متعددة لكل شركة

### 🔄 العمل المزدوج (أونلاين/أوفلاين)
- **وضع الأونلاين**: مزامنة فورية مع السيرفر المركزي
- **وضع الأوفلاين**: عمل كامل بدون إنترنت مع مزامنة لاحقة
- نظام Sync ذكي لحل التعارضات

### 🔐 نظام الترخيص المتقدم
- ترخيص يعتمد على Hardware ID
- تشفير متقدم للبيانات
- دعم التفعيل الأوفلاين بكود
- تحديث تلقائي للتراخيص

### 💼 خطط الاشتراكات المرنة
- خطط قابلة للتخصيص بالكامل
- تحكم دقيق في الميزات والصلاحيات
- إدارة عدد المستخدمين والفروع
- تحديد حدود المستندات والطباعة

### 📊 وحدات ERP المتكاملة
- **المشتريات**: أوامر الشراء، الموردين، الاستلام
- **المخزون**: الأصناف، المستودعات، الحركات المخزنية
- **المحاسبة**: دليل الحسابات، القيود المحاسبية
- **الأبعاد المالية**: مراكز التكلفة، المشاريع
- **التصنيع**: (قيد التطوير)
- **الأصول الثابتة**: (قيد التطوير)

## الهيكل التقني

### Backend
- **FastAPI**: إطار العمل REST API
- **SQLAlchemy**: ORM للتعامل مع قواعد البيانات
- **Alembic**: إدارة المigrations
- **PostgreSQL**: قاعدة البيانات الرئيسية
- **SQLite**: قاعدة بيانات الأوفلاين

### الأمان
- **JWT**: مصادقة المستخدمين
- **Cryptography**: تشفير التراخيص والبيانات الحساسة
- **Bcrypt**: تشفير كلمات المرور

## التثبيت والإعداد

### المتطلبات
- Python 3.8+
- PostgreSQL 12+ (للوضع الأونلاين)
- Git

### خطوات التثبيت

1. **استنساخ المشروع**
```bash
git clone <repository-url>
cd HaggagHub
```

2. **إنشاء البيئة الافتراضية**
```bash
python -m venv .venv
.venv\Scripts\Activate  # في Windows
source .venv/bin/activate  # في Linux/Mac
```

3. **تثبيت الحزم**
```bash
pip install -r requirements.txt
```

4. **إعداد متغيرات البيئة**
```bash
cp .env.example .env
# قم بتعديل .env بالقيم المناسبة
```

5. **إعداد قاعدة البيانات**
```bash
alembic upgrade head
```

6. **تشغيل التطبيق**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## استخدام الـ API

### المصادقة
```bash
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password",
    "tenant_code": "company1"
  }'
```

### إنشاء مستأجر جديد
```bash
curl -X POST "http://localhost:8080/api/v1/tenants" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "شركة مثال",
    "code": "example-co",
    "contact_email": "info@example.com",
    "currency_code": "EGP"
  }'
```

### إنشاء خطة اشتراك
```bash
curl -X POST "http://localhost:8080/api/v1/subscription-plans" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "الخطة الاحترافية",
    "code": "professional",
    "monthly_price": 299.99,
    "max_users": 10,
    "max_branches": 5,
    "can_access_purchases": true,
    "can_access_inventory": true,
    "can_access_accounting": true
  }'
```

### التحقق من الترخيص
```bash
curl -X POST "http://localhost:8080/api/v1/licenses/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "hardware_id": "abc123...",
    "license_key": "encrypted_key_here..."
  }'
```

## نظام الترخيص الأوفلاين

### إنشاء ترخيص أوفلاين
```python
from core.services.license_service import LicenseService

license_service = LicenseService()
hardware_id = license_service.get_hardware_id()
license_key = license_service.generate_license_key(
    hardware_id=hardware_id,
    expiry_date=datetime(2024, 12, 31),
    subscription_plan_id="plan_id_here"
)
```

### التحقق من الترخيص الأوفلاين
```python
is_valid, data = license_service.verify_license(license_key, hardware_id)
if is_valid:
    print("License valid until:", data['expiry_date'])
else:
    print("Invalid license:", data['error'])
```

## المزامنة بين الأوفلاين والأونلاين

### الحصول على حالة المزامنة
```bash
curl -X GET "http://localhost:8080/api/v1/sync/status" \
  -H "Authorization: Bearer <token>"
```

### رفع البيانات للسيرفر
```bash
curl -X POST "http://localhost:8080/api/v1/sync/upload" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [...],
    "tenant_id": "tenant_id_here"
  }'
```

## توثيق الـ API

بعد تشغيل التطبيق، يمكنك زيارة:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## هيكل المشروع

```
HaggagHub/
├── core/                          # الكود الأساسي
│   ├── models/                    # نماذج قاعدة البيانات
│   │   ├── entities/              # الكيانات الرئيسية
│   │   └── base/                 # النماذج الأساسية
│   ├── services/                  # خدمات الأعمال
│   └── schemas/                   # Pydantic schemas
├── api/                          # API endpoints
│   └── v1/                       # الإصدار الأول من الـ API
├── database/                      # إعدادات قاعدة البيانات
├── alembic/                       # Database migrations
├── main.py                        # نقطة دخول التطبيق
├── config.py                      # إعدادات التطبيق
└── requirements.txt               # الحزم المطلوبة
```

## التطوير المستقبلي

### الميزات القادمة
- واجهة مستخدم بـ Flutter
- نظام تقارير متقدم
- دعم متعدد اللغات
- نظام إشعارات
- تكامل مع أنظمة خارجية
- نظام عملة متعدد
- نظام نسخ احتياطي تلقائي

### التحسينات التقنية
- تحسين أداء المزامنة
- إضافة Redis caching
- تحسين الأمان
- إضافة unit tests
- تحسين التوثيق

## المساهمة

1. Fork المشروع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. عمل commit للتغييرات (`git commit -m 'Add some AmazingFeature'`)
4. دفع الفرع (`git push origin feature/AmazingFeature`)
5. إنشاء Pull Request

## الترخيص

هذا المشروع مرخص تحت ترخيص MIT - راجع ملف LICENSE للتفاصيل.

## الدعم

لأي استفسارات أو مشاكل:
- البريد الإلكتروني: support@haggaghub.com
- التوثيق: [Documentation Link]
- الإبلاغ عن مشاكل: [Issues Link]

---

**HaggagHub ERP** - حل متكامل لإدارة الأعمال
