from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.roadmap import Roadmap
from app.models.booking import Booking, BookingStatus
from app.models.content import Content
from app.core.security import decode_access_token
from app.schemas.admin import (
    AdminStats,
    UserUpdateByAdmin,
    UserResponseByAdmin,
    ContentCreateByAdmin,
    ContentUpdateByAdmin,
)


router = APIRouter(prefix="/admin", tags=["Admin"])


def get_current_admin(token: str, db: Session):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized as admin")

    return user


@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    total_users = db.query(User).count()
    total_mentors = db.query(User).filter(User.is_mentor == True).count()
    total_students = db.query(User).filter(User.is_mentor == False).count()
    total_roadmaps = db.query(Roadmap).count()
    total_bookings = db.query(Booking).count()
    completed_roadmaps = db.query(Roadmap).filter(Roadmap.is_completed == 1).count()
    pending_bookings = db.query(Booking).filter(Booking.status == BookingStatus.PENDING).count()

    total_revenue = 0

    return AdminStats(
        total_users=total_users,
        total_mentors=total_mentors,
        total_students=total_students,
        total_roadmaps=total_roadmaps,
        total_bookings=total_bookings,
        completed_roadmaps=completed_roadmaps,
        total_revenue=total_revenue,
        pending_bookings=pending_bookings,
    )


@router.get("/users", response_model=List[UserResponseByAdmin])
def get_all_users(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponseByAdmin)
def get_user(
    user_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=UserResponseByAdmin)
def update_user(
    user_id: int,
    user_data: UserUpdateByAdmin,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.is_admin is not None:
        user.is_admin = user_data.is_admin
    if user_data.is_mentor is not None:
        user.is_mentor = user_data.is_mentor
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.subscription_type is not None:
        user.subscription_type = user_data.subscription_type

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
        db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.post("/content", response_model=ContentCreateByAdmin)
def create_content(
    content_data: ContentCreateByAdmin,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    new_content = Content(
        roadmap_id=content_data.roadmap_id,
        stage_number=content_data.stage_number,
        title=content_data.title,
        description=content_data.description,
        content_type=content_data.content_type,
        content_url=content_data.content_url,
        is_required=content_data.is_required,
        order=content_data.order,
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content


@router.put("/content/{content_id}", response_model=ContentUpdateByAdmin)
def update_content(
    content_id: int,
    content_data: ContentUpdateByAdmin,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content_data.title is not None:
        content.title = content_data.title
    if content_data.description is not None:
        content.description = content_data.description
    if content_data.content_type is not None:
        content.content_type = content_data.content_type
    if content_data.content_url is not None:
        content.content_url = content_data.content_url
    if content_data.is_required is not None:
        content.is_required = content_data.is_required
    if content_data.order is not None:
        content.order = content_data.order

    db.commit()
    db.refresh(content)
    return content


@router.delete("/content/{content_id}")
def delete_content(
    content_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    admin = get_current_admin(token, db)

    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    db.delete(content)
    db.commit()
    return {"message": "Content deleted successfully"}
    