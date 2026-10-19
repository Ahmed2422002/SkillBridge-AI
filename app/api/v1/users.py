from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin 
from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

# ==========================================
# 1. مسار التسجيل (Sign Up)
# ==========================================
@router.post("/auth/student/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    # التأكد أن الإيميل غير مسجل مسبقاً
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # إنشاء مستخدم جديد
    new_user = User(
        username=user.username,         
        full_name=user.full_name,       
        email=user.email,
        password_hash=get_password_hash(user.password) 
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# ==========================================
# 2. مسار تسجيل الدخول (Login)
# ==========================================
@router.post("/auth/student/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    
    # البحث عن المستخدم بالايميل
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    # إذا لم يوجد المستخدم
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # التحقق من كلمة المرور (تمت إضافة try/except لمنع انهيار السيرفر)
    try:
        is_password_correct = verify_password(user_credentials.password, user.password_hash)
    except Exception:
        is_password_correct = False # إذا كان الباسورد القديم تالف، نعتبره خطأ
        
    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # إنشاء التوكن
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=timedelta(minutes=60)
    )
    
    # إرجاع الاستجابة للفرونت إند
    return {
        "message": "Login successful", 
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user.username,  
            "full_name": user.full_name, 
            "email": user.email
        }
        }
