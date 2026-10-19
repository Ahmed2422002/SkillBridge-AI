from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# إعدادات CORS مفتوحة بالكامل للتجربة (كما طلبت)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# 1. المسار الجديد اللي أنت كتبته
@app.post("/auth/student/signup")
async def signup(user: UserRegister):
    print(f"✅✅✅ وصل الطلب للتسجيل (المسار الجديد)! البيانات: {user}")
    return {"message": "Success", "user": user.name}

# 2. المسار القديم (الاحتياطي)
@app.post("/api/v1/register")
async def register(user: UserRegister):
    print(f"✅✅✅ وصل الطلب للتسجيل (المسار القديم)! البيانات: {user}")
    return {"message": "Success", "user": user.name}

# مسار إضافي للفحص السريع
@app.get("/")
def read_root():
    return {"status": "Backend is running perfectly!"}
