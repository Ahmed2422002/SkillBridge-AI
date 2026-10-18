from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="SkillBridge AI")

# 1. إعدادات CORS (لازم تكون قبل أي Route)
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

# 2. نماذج البيانات
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# 3. المسار السري (المصيدة) - هاد اللي رح يحل مشكلة الـ 404
@app.post("/auth/student/signup")
async def fallback_signup(user: UserRegister):
    print(f"✅✅✅ تم استقبال بيانات: {user.email} ✅✅✅")
    return {"message": "User registered successfully", "email": user.email}

# 4. المسارات الأصلية (الصحيحة)
@app.post("/api/v1/register")
async def register(user: UserRegister):
    return {"message": "User registered successfully", "email": user.email}

@app.post("/api/v1/login")
async def login(user: UserLogin):
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}

@app.get("/")
async def root():
    return {"status": "Backend is working perfectly!"}
