from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash
from datetime import timedelta

router = APIRouter()

# ⚠️ هنا السر: غيرنا المسار ليطابق الفرونت إند
@router.post("/auth/student/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    # التأكد أن الإيميل غير مسجل مسبقاً
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # إنشاء مستخدم جديد (هذا الجزء يعتمد على كيفية تعريفك للـ User في models)
    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password) # تأكد من استخدام اسم الحقل الصحيح (hashed_password أو password_hash)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
