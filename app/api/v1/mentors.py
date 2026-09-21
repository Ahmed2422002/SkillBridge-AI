from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.mentor import Mentor
from app.models.booking import Booking, BookingStatus
from app.schemas.mentor import (
    MentorCreate,
    MentorUpdate,
    MentorResponse,
    BookingCreate,
    BookingUpdate,
    BookingResponse,
    MentorSearch,
)
from app.core.security import decode_access_token


router = APIRouter(prefix="/mentors", tags=["Mentors"])


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
# 1. إنشاء مرشد جديد (POST)
# ============================================
@router.post("/", response_model=MentorResponse)
def create_mentor(
    mentor: MentorCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    # التأكد إن المستخدم مش مرشد مسبقاً
    existing = db.query(Mentor).filter(Mentor.user_id == user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User is already a mentor")

    new_mentor = Mentor(
        user_id=user.id,
        specialty=mentor.specialty,
        experience_years=mentor.experience_years,
        hourly_rate=mentor.hourly_rate,
        bio=mentor.bio,
        is_available=True,
        rating=0,
    )
    db.add(new_mentor)
    db.commit()
    db.refresh(new_mentor)
    return new_mentor


# ============================================
# 2. جلب كل المرشدين (GET)
# ============================================
@router.get("/", response_model=List[MentorResponse])
def get_mentors(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    mentors = db.query(Mentor).all()
    return mentors


# ============================================
# 3. جلب مرشد واحد بالـ ID (GET)
# ============================================
@router.get("/{mentor_id}", response_model=MentorResponse)
def get_mentor(
    mentor_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    return mentor


# ============================================
# 4. تحديث مرشد (PUT)
# ============================================
@router.put("/{mentor_id}", response_model=MentorResponse)
def update_mentor(
    mentor_id: int,
    mentor_data: MentorUpdate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    if mentor.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if mentor_data.specialty is not None:
        mentor.specialty = mentor_data.specialty
    if mentor_data.experience_years is not None:
        mentor.experience_years = mentor_data.experience_years
    if mentor_data.hourly_rate is not None:
        mentor.hourly_rate = mentor_data.hourly_rate
    if mentor_data.bio is not None:
        mentor.bio = mentor_data.bio
    if mentor_data.is_available is not None:
        mentor.is_available = mentor_data.is_available
        db.commit()
    db.refresh(mentor)
    return mentor


# ============================================
# 5. حذف مرشد (DELETE)
# ============================================
@router.delete("/{mentor_id}")
def delete_mentor(
    mentor_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    if mentor.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(mentor)
    db.commit()
    return {"message": "Mentor deleted successfully"}


# ============================================
# 6. البحث عن مرشدين (POST)
# ============================================
@router.post("/search", response_model=List[MentorResponse])
def search_mentors(
    search: MentorSearch,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    query = db.query(Mentor)
    if search.specialty:
        query = query.filter(Mentor.specialty.ilike(f"%{search.specialty}%"))
    if search.min_rating:
        query = query.filter(Mentor.rating >= search.min_rating)

    mentors = query.all()
    return mentors


# ============================================
# 7. حجز جلسة مع مرشد (POST)
# ============================================
@router.post("/bookings/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    # التأكد إن المرشد موجود
    mentor = db.query(Mentor).filter(Mentor.id == booking.mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    # التأكد إن المستخدم مش بيحجز مع نفسه
    if mentor.user_id == user.id:
        raise HTTPException(status_code=400, detail="Cannot book yourself")

    new_booking = Booking(
        student_id=user.id,
        mentor_id=booking.mentor_id,
        booking_date=booking.booking_date,
        start_time=booking.start_time,
        end_time=booking.end_time,
        status=BookingStatus.PENDING,
        notes=booking.notes,
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# ============================================
# 8. جلب كل حجوزاتي (GET)
# ============================================
@router.get("/bookings/my", response_model=List[BookingResponse])
def get_my_bookings(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    bookings = db.query(Booking).filter(Booking.student_id == user.id).all()
    return bookings


# ============================================
# 9. تحديث حجز (PUT)
# ============================================
@router.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.student_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if booking_data.status is not None:
        booking.status = booking_data.status
    if booking_data.notes is not None:
        booking.notes = booking_data.notes

    db.commit()
    db.refresh(booking)
    return booking


# ============================================
# 10. حذف حجز (DELETE)
# ============================================
@router.delete("/bookings/{booking_id}")
def delete_booking(
    booking_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.student_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}