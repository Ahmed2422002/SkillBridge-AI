from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.v1 import api_router
from app.core.database import Base, engine

app = FastAPI(title="SkillBridge AI", version="1.0.0")

# إنشاء الجداول (كل الموديلات لازم تكون مستوردة قبل هالسطر، وهي مستوردة عبر الـ routers)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"❌ خطأ في البيانات المرسلة: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )


app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "SkillBridge AI API is running"}


@app.get("/test")
def test():
    return {"status": "working"}
