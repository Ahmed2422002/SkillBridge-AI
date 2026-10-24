import re
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.mentor import Mentor
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin

router = APIRouter()


# ---------- أدوات مساعدة ----------
def _unique_username(db: Session, wanted: Optional[str]) -> str:
    base = re.sub(r"[^a-zA-Z0-9_.-]", "", (wanted or "").replace(" ", "")) or "user"
    candidate, n = base, 1
    while db.query(User).filter(User.username == candidate).first():
        n += 1
        candidate = f"{base}{n}"
    return candidate


def _auth_response(user: User, message: str) -> dict:
    token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=60)
    )
    return {
        "message": message,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "is_mentor": bool(user.is_mentor),
        },
    }


def _check_password(plain: str, hashed: str) -> bool:
    try:
        return verify_password(plain, hashed)
    except Exception:
        return False


# ---------- الطالب ----------
@router.post(
    "/auth/student/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def student_signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    username = _unique_username(db, user.username or user.email.split("@")[0])
    new_user = User(
        username=username,
        full_name=user.full_name or user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/auth/student/login")
def student_login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not _check_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return _auth_response(user, "Login successful")


# ---------- المنتور ----------
class MentorSignupIn(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    title: Optional[str] = None
    expertise: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    bio: Optional[str] = None


@router.post("/auth/mentor/signup", status_code=status.HTTP_201_CREATED)
def mentor_signup(data: MentorSignupIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=_unique_username(db, data.email.split("@")[0]),
        full_name=data.fullName,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        is_mentor=True,
    )
    db.add(user)
    db.flush()

    db.add(
        Mentor(
            user_id=user.id,
            specialty=data.expertise or data.title or "General",
            experience_years=0,
            hourly_rate=0.0,
            bio=data.bio,
        )
    )
    db.commit()
    db.refresh(user)
    return _auth_response(user, "Mentor account created")


@router.post("/auth/mentor/login")
def mentor_login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not _check_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_mentor:
        raise HTTPException(status_code=403, detail="This account is not a mentor account")
    return _auth_response(user, "Login successful")
