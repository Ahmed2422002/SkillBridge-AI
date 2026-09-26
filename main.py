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

app = FastAPI(
    title="SkillBridge AI API",
    description="منصة تعلم ذكية باستخدام الذكاء الاصطناعي",
    version="1.0.0"
)

# إعداد CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تسجيل المسارات
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(roadmaps.router, prefix="/roadmaps", tags=["Roadmaps"])
app.include_router(survey.router, prefix="/survey", tags=["Survey"])
app.include_router(content.router, prefix="/content", tags=["Content"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
app.include_router(mentors.router, prefix="/mentors", tags=["Mentors"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(progress.router, prefix="/progress", tags=["Progress"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SkillBridge AI Platform!"}

@app.get("/test")
def test():
    return {"message": "Test successful"}
