from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.database import Base, engine

app = FastAPI(title="SkillBridge AI", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط كل الـ Routers الأصلية
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "SkillBridge AI API is running"}

@app.get("/test")
def test():
    return {"status": "working"}
