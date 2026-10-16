from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.database import Base, engine  # ⚠️ مهم عشان ينشئ الجداول

# إنشاء التطبيق
app = FastAPI(title="SkillBridge AI", version="1.0.0")

# إنشاء جداول قاعدة البيانات تلقائياً لو مش موجودة
Base.metadata.create_all(bind=engine)

# إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # ⚠️ مهم جداً: خليها False مع النجمة
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط كل الـ Routers
app.include_router(api_router, prefix="/api/v1")


# اختبار بسيط للسيرفر
@app.get("/")
def read_root():
    return {"message": "SkillBridge AI API is running"}


@app.get("/test")
def test():
    return {"status": "working"}
