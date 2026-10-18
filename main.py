from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="SkillBridge AI",
    version="1.0.0",
    description="Backend for SkillBridge AI platform"
)

# ==========================================
# 1. إعدادات CORS (أهم جزء لحل المشكلة)
# ==========================================
# لازم تحط رابط Vercel تبعك بالضبط، وبدون / في الآخر
origins = [
    "https://skill-bridge-frontend-flame.vercel.app",
    "http://localhost:3000",  # للتطوير المحلي
    "http://localhost:5173",  # للتطوير المحلي (Vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. نماذج البيانات (Pydantic Models)
# ==========================================
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Mentor(BaseModel):
    name: str
    expertise: str

# ==========================================
# 3. المسارات (Routes) - تأكد من البادئة /api/v1
# ==========================================
# بناءً على صورة الـ Swagger، المسار هو /api/v1/register
# إذا الفرونت إند يبعت لـ /api/v1/register، لازم نطابق هذا المسار

@app.post("/api/v1/register", tags=["Auth"])
async def register(user: UserRegister):
    # هنا بتحط منطق التسجيل (حفظ بالداتابيز)
    # مثال مبدئي:
    return {"message": "User registered successfully", "user": user.email}

@app.post("/api/v1/login", response_model=Token, tags=["Auth"])
async def login(user: UserLogin):
    # هنا بتحط منطق التحقق من الإيميل والباسورد
    # مثال مبدئي (للتجربة فقط، لا تستخدمه بالإنتاج):
    if user.email and user.password:
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@app.get("/api/v1/me", tags=["Auth"])
async def read_users_me():
    return {"user": "current_user_info"}

# ==========================================
# 4. مسارات المينتورز (Mentors) - موجودة بالـ Swagger
# ==========================================
@app.get("/api/v1/mentors/", tags=["Mentors"])
async def get_mentors():
    return [{"id": 1, "name": "Mentor 1", "expertise": "Python"}]

@app.post("/api/v1/mentors/", tags=["Mentors"])
async def create_mentor(mentor: Mentor):
    return {"message": "Mentor created", "mentor": mentor}

# ==========================================
# 5. مسار الصحة (Health Check) - مفيد لـ Render
# ==========================================
@app.get("/")
async def root():
    return {"status": "healthy", "service": "SkillBridge AI"}

@app.get("/test")
async def test():
    return {"status": "test endpoint works"}
