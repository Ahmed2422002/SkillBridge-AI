import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env مباشرة
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine

# استيراد جميع المسارات
from app.api.v1 import auth, roadmaps, survey, content, quizzes, mentors, admin, progress

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

# إضافة redirect_slashes=False لمنع مشكلة الـ 307 Redirect التي تكسر الـ CORS
app = FastAPI(
    title="SkillBridge AI API",
    description="منصة تعلم ذكية باستخدام الذكاء الاصطناعي",
    version="1.0.0",
    redirect_slashes=False
)

# إعداد CORS
origins = [
    "https://skill-bridge-frontend-flame.vercel.app", # رابط موقعك
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل المسارات
app.include_router(auth.router, prefix="/auth")
app.include_router(roadmaps.router, prefix="/roadmaps")
app.include_router(survey.router, prefix="/survey")
app.include_router(content.router, prefix="/content")
app.include_router(quizzes.router, prefix="/quizzes")
app.include_router(mentors.router, prefix="/mentors")
app.include_router(admin.router, prefix="/admin")
app.include_router(progress.router, prefix="/progress")

@app.get("/")
def read_root():
    return {"message": "Welcome to SkillBridge AI API"}

@app.get("/test")
def test():
    return {"message": "Test successful"}
