import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env مباشرة
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

# استيراد جميع المسارات
from app.api.v1 import auth, roadmaps, survey, content # (تأكد من إضافة باقي الملفات اللي عندك هنا)

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

# إضافة redirect_slashes=False لمنع مشكلة الـ 307 Redirect
app = FastAPI(
    title="SkillBridge AI API",
    description="منصة تعلم ذكية باستخدام الذكاء الاصطناعي",
    version="1.0.0",
    redirect_slashes=False
)

# إعداد CORS (السماح لجميع روابط Vercel والـ Localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:3000|http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (باقي كود الـ Endpoints والـ Routes بتاعتك يكمل من هنا زي ما هو)
