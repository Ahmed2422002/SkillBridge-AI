from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


# ============================================
# 1. تسجيل مستخدم جديد
# ============================================
@router.post("/register")
def register(
    email: str,
    username: str,
    password: str,
    full_name: str = None,
    db: Session = Depends(get_db)
):
    # التحقق إذا المستخدم موجود
    existing = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )

    # إنشاء المستخدم الجديد
    new_user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        is_active=True,
        is_admin=False,
        is_mentor=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


# ============================================
# 2. تسجيل الدخول
# ============================================
@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
    }


# ============================================
# 3. جلب بيانات المستخدم الحالي
# ============================================
@router.get("/me")
def get_me(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
    }


# ============================================
# 4. تحديث بيانات المستخدم (PUT)
# ============================================
@router.put("/me")
def update_me(
    full_name: str = None,
    email: str = None,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if full_name is not None:
        user.full_name = full_name
    if email is not None:
        user.email = email

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
    }
