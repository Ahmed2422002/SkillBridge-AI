from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.v1 import api_router
from app.core.database import Base, engine

app = FastAPI(title="SkillBridge AI", version="1.0.0")

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

# إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✨ هذا الجزء الجديد: اعتراض أخطاء البيانات وطباعتها
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # هذا السطر سيطبع الخطأ في سجلات Render لكي نعرف الحقل الناقص
    print(f"❌ خطأ في البيانات المرسلة: {exc.errors()}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )

# ربط كل الـ Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "SkillBridge AI API is running"}

@app.get("/test")
def test():
    return {"status": "working"}
