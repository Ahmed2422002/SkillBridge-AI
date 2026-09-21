from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api.v1 import auth, roadmaps, survey, content, quizzes, mentors, admin

# ============================================
# إنشاء جداول قاعدة البيانات
# ============================================
Base.metadata.create_all(bind=engine)

# ============================================
# إنشاء تطبيق FastAPI
# ============================================
app = FastAPI(
    title="SkillBridge AI API",
    description="منصة تعلم ذكية باستخدام الذكاء الاصطناعي",
    version="1.0.0"
)

# ============================================
# إعداد CORS (مهم جداً للربط مع الـ Frontend)
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج، حدد الدومينات المسموحة مثل ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# تسجيل الـ Routers (المسارات)
# ============================================
app.include_router(auth.router)
app.include_router(roadmaps.router)
app.include_router(survey.router)
app.include_router(content.router)
app.include_router(quizzes.router)
app.include_router(mentors.router)
app.include_router(admin.router)

# ============================================
# المسارات الأساسية
# ============================================
@app.get("/")
def read_root():
    return {"message": "Welcome to SkillBridge AI Platform!"}

@app.get("/test")
def test():
    return {"message": "Test successful"}
