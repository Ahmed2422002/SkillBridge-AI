from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # للتجربة عشان نلغي أي مشكلة CORS
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# هاد المسار اللي الفرونت إند عم يدور عليه بالضبط
@app.post("/auth/student/signup")
async def signup(user: UserRegister):
    print("✅✅✅ وصل الطلب للتسجيل بنجاح! ✅✅✅")
    return {"message": "Success"}

# هاد المسار الأصلي تبعك للاحتياط
@app.post("/api/v1/register")
async def register(user: UserRegister):
    return {"message": "Success"}
