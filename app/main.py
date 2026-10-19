from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.database import Base, engine  
from pydantic import BaseModel # تمت إضافة هذا السطر لتعريف البيانات

# إنشاء التطبيق
app = FastAPI(title="SkillBridge AI", version="1.0.0")

# إنشاء جداول قاعدة البيانات تلقائياً لو مش موجودة
Base.metadata.create_all(bind=engine)

# إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ✨ إضافة مسار التسجيل المباشر هنا ✨
# ==========================================
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

@app.post("/api/v1/auth/student/signup")
async def direct_signup(user: UserRegister):
    print(f"✅✅✅ وصل الطلب للمسار الجديد! البيانات: {user}")
    return {"message": "Success", "user": user.name}
# ==========================================

# ربط كل الـ Routers الأصلية (لن تتأثر)
app.include_router(api_router, prefix="/api/v1")

# اختبار بسيط للسيرفر
@app.get("/")
def read_root():
    return {"message": "SkillBridge AI API is running"}

@app.get("/test")
def test():
    return {"status": "working"}
