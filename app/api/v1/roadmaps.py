from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.roadmap import Roadmap
from app.schemas.roadmap import (
    RoadmapCreate,
    RoadmapUpdate,
    RoadmapResponse,
)
from app.core.security import decode_access_token


router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])


# ============================================
# دالة مساعدة: جلب المستخدم من التوكن
# ============================================
def get_current_user(token: str, db: Session):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# ============================================
# 1. إنشاء خطة جديدة (POST)
# ============================================
@router.post("/", response_model=RoadmapResponse)
def create_roadmap(
    roadmap: RoadmapCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    new_roadmap = Roadmap(
        user_id=user.id,
        title=roadmap.title,
        description=roadmap.description,
        goal=roadmap.goal,
        level=roadmap.level,
        steps=roadmap.steps,
        progress=0,
        is_completed=0,
    )
    db.add(new_roadmap)
    db.commit()
    db.refresh(new_roadmap)
    return new_roadmap
    # ============================================
# 2. جلب كل الخطط (GET)
# ============================================
@router.get("/", response_model=List[RoadmapResponse])
def get_roadmaps(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    roadmaps = db.query(Roadmap).filter(Roadmap.user_id == user.id).all()
    return roadmaps


# ============================================
# 3. جلب خطة واحدة (GET)
# ============================================
@router.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap(
    roadmap_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if roadmap.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return roadmap


# ============================================
# 4. تحديث خطة (PUT)
# ============================================
@router.put("/{roadmap_id}", response_model=RoadmapResponse)
def update_roadmap(
    roadmap_id: int,
    roadmap_data: RoadmapUpdate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if roadmap.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if roadmap_data.title is not None:
        roadmap.title = roadmap_data.title
    if roadmap_data.description is not None:
        roadmap.description = roadmap_data.description
    if roadmap_data.goal is not None:
        roadmap.goal = roadmap_data.goal
    if roadmap_data.level is not None:
        roadmap.level = roadmap_data.level
    if roadmap_data.steps is not None:
        roadmap.steps = roadmap_data.steps
    if roadmap_data.progress is not None:
        roadmap.progress = roadmap_data.progress
    if roadmap_data.is_completed is not None:
        roadmap.is_completed = roadmap_data.is_completed

    db.commit()
    db.refresh(roadmap)
    return roadmap


# ============================================
# 5. حذف خطة (DELETE)
# ============================================
@router.delete("/{roadmap_id}")
def delete_roadmap(
    roadmap_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if roadmap.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(roadmap)
    db.commit()
    return {"message": "Roadmap deleted successfully"}