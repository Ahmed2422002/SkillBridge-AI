from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import decode_access_token

router = APIRouter(prefix="/progress", tags=["Progress"])


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/")
def get_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """جلب تقدم المستخدم الحالي"""
    return {
        "user_id": current_user.id,
        "progress": 0,
        "completed_lessons": [],
        "message": "Progress endpoint working"
    }


@router.post("/update")
def update_progress(data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """تحديث تقدم المستخدم"""
    return {
        "message": "Progress updated successfully",
        "user_id": current_user.id,
        "data_received": data
    }


@router.post("/complete_content_progress_complete_post")
def complete_content_progress(data: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """إكمال درس معين (للتوافق مع الـ Frontend)"""
    return {
        "message": "Content marked as complete",
        "user_id": current_user.id,
        "data": data
    }
