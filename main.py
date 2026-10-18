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
origins = [
    "https://skill-bridge-frontend-flame.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
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
# 3. الدوال الأساسية (Business Logic)
# ==========================================
async def register_logic(user: UserRegister):
    # هنا بتحط منطق التسجيل (حفظ بالداتابيز)
    return {"message": "User registered successfully", "user": user.email}

async def login_logic(user: UserLogin):
    if user.email and user.password:
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

# ==========================================
# 4. المسارات (Routes) 
# ==========================================

# --- المسارات الأصلية (اللي كانت عندك) ---
@app.post("/api/v1/register", tags=["Auth"])
async def register(user: UserRegister):
    return await register_logic(user)

@app.post("/api/v1/login", response_model=Token, tags=["Auth"])
async def login(user: UserLogin):
    return await login_logic(user)

# --- المسارات البديلة (عشان نمسك الفرونت إند اللي بيبعت مسارات غلط) ---
# بناءً على الـ Logs، الفرونت بيبعت لـ /auth/student/signup
@app.post("/auth/student/signup", tags=["Fallback Auth"])
async def fallback_signup(user: UserRegister):
    return await register_logic(user)

# وهاي مسارات بديلة للتسجيل والدخول عشان نضرب عصفورين بحجر
@app.post("/auth/signup", tags=["Fallback Auth"])
async def fallback_signup_2(user: UserRegister):
    return await register_logic(user)

@app.post("/auth/login", tags=["Fallback Auth"])
async def fallback_login(user: UserLogin):
    return await login_logic(user)


# ==========================================
# 5. مسارات المينتورز (Mentors)
# ==========================================
@app.get("/api/v1/mentors/", tags=["Mentors"])
async def get_mentors():
    return [{"id": 1, "name": "Mentor 1", "expertise": "Python"}]

@app.post("/api/v1/mentors/", tags=["Mentors"])
async def create_mentor(mentor: Mentor):
    return {"message": "Mentor created", "mentor": mentor}

# ==========================================
# 6. مسار الصحة (Health Check)
# ==========================================
@app.get("/")
async def root():
    return {"status": "healthy", "service": "SkillBridge AI"}

@app.get("/test")
async def test():
    return {"status": "test endpoint works"}
