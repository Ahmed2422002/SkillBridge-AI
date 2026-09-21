from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ============================================
# مخططات المرشد (Mentor)
# ============================================
class MentorCreate(BaseModel):
    specialty: str
    experience_years: int
    hourly_rate: float
    bio: Optional[str] = None


class MentorUpdate(BaseModel):
    specialty: Optional[str] = None
    experience_years: Optional[int] = None
    hourly_rate: Optional[float] = None
    bio: Optional[str] = None
    is_available: Optional[bool] = None


class MentorResponse(BaseModel):
    id: int
    user_id: int
    specialty: str
    experience_years: int
    hourly_rate: float
    bio: Optional[str] = None
    is_available: bool
    rating: float
    total_reviews: int
    created_at: datetime   # ← التعديل هنا (كان str)

    class Config:
        from_attributes = True


class MentorSearch(BaseModel):
    specialty: Optional[str] = None
    min_rating: Optional[float] = None


# ============================================
# مخططات الحجز (Booking)
# ============================================
class BookingCreate(BaseModel):
    mentor_id: int
    booking_date: str  # أو date
    start_time: str    # أو time
    end_time: str
    notes: Optional[str] = None


class BookingUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    student_id: int
    mentor_id: int
    booking_date: str
    start_time: str
    end_time: str
    status: str
    notes: Optional[str] = None
    created_at: datetime   # ← تأكد إنه datetime (إذا موجود)

    class Config:
        from_attributes = True
