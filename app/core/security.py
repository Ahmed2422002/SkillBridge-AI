from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# ============================================
# إعداد تشفير كلمات المرور
# ============================================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================================
# 1. التحقق من كلمة المرور
# ============================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """التحقق من كلمة المرور"""
    return pwd_context.verify(plain_password, hashed_password)

# ============================================
# 2. تشفير كلمة المرور
# ============================================
def get_password_hash(password: str) -> str:
    """تشفير كلمة المرور"""
    return pwd_context.hash(password)

# ============================================
# 3. إنشاء التوكن (JWT)
# ============================================
def create_access_token(data: dict):
    """إنشاء توكن JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ============================================
# 4. فك تشفير التوكن (هذي الدالة الناقصة)
# ============================================
def decode_access_token(token: str):
    """فك تشفير التوكن واستخراج البيانات منه"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
