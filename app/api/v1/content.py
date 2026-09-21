from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.content import Content
from app.models.roadmap import Roadmap
from app.models.user import User
from app.schemas.content import ContentCreate, ContentResponse

router = APIRouter(prefix="/content", tags=["Content"])


# ============================================
# دالة مساعدة: جلب المستخدم الحالي من التوكن
# ============================================
def get_current_user(token: str, db: Session):
    from app.core.security import decode_access_token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============================================
# 1. إنشاء محتوى جديد (للمشرف)
# ============================================
@router.post("/", response_model=ContentResponse)
def create_content(
    content: ContentCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    roadmap = db.query(Roadmap).filter(Roadmap.id == content.roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if roadmap.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    new_content = Content(
        roadmap_id=content.roadmap_id,
        stage_number=content.stage_number,
        title=content.title,
        description=content.description,
        content_type=content.content_type,
        content_url=content.content_url,
        is_required=content.is_required,
        order=content.order,
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content


# ============================================
# 2. جلب كل المحتوى الخاص بـ Roadmap معينة
# ============================================
@router.get("/roadmap/{roadmap_id}", response_model=List[ContentResponse])
def get_contents_by_roadmap(
    roadmap_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    roadmap = db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if roadmap.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    contents = db.query(Content).filter(Content.roadmap_id == roadmap_id).all()
    return contents


# ============================================
# 3. جلب محتوى واحد بالـ ID
# ============================================
@router.get("/{content_id}", response_model=ContentResponse)
def get_content(
    content_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    roadmap = db.query(Roadmap).filter(Roadmap.id == content.roadmap_id).first()
    if roadmap.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
        return content


# ============================================
# 4. تحديث محتوى (للمشرف)
# ============================================
@router.put("/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: int,
    content_data: ContentCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    roadmap = db.query(Roadmap).filter(Roadmap.id == content.roadmap_id).first()
    if roadmap.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    content.title = content_data.title
    content.description = content_data.description
    content.content_type = content_data.content_type
    content.content_url = content_data.content_url
    content.is_required = content_data.is_required
    content.order = content_data.order

    db.commit()
    db.refresh(content)
    return content


# ============================================
# 5. حذف محتوى (للمشرف)
# ============================================
@router.delete("/{content_id}")
def delete_content(
    content_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    roadmap = db.query(Roadmap).filter(Roadmap.id == content.roadmap_id).first()
    if roadmap.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(content)
    db.commit()
    return {"message": "Content deleted successfully"}