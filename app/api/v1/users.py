from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin # تأكد أن UserLogin موجود في السكيما
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
        name=user.name,
        email=user.email,
        # ⚠️ ملاحظة هامة: إذا كان حقل كلمة المرور في موديل المستخدم اسمه hashed_password، غير الكلمة أدناه
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
    
    # إذا لم يوجد المستخدم أو كلمة المرور غير صحيحة
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # التحقق من كلمة المرور (تأكد من اسم الحقل في الموديل password_hash أو hashed_password)
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # إنشاء التوكن (إذا كان نظامك يستخدم JWT)
    # access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    
    # إرجاع استجابة بسيطة (يمكنك تعديلها حسب ما يتوقعه الفرونت إند)
    return {"message": "Login successful", "user": user.name, "email": user.email}
