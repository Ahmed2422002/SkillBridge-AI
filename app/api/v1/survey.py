from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/survey", tags=["Survey"])


# ============================================
# 1. جلب كل الاستبيانات (مبدئي)
# ============================================
@router.get("/")
def get_surveys(db: Session = Depends(get_db)):
    return {"message": "Survey endpoint working", "surveys": []}


# ============================================
# 2. جلب أسئلة استبيان معين (مبدئي)
# ============================================
@router.get("/{survey_id}/questions")
def get_questions(survey_id: int):
    return {"survey_id": survey_id, "questions": []}


# ============================================
# 3. إرسال إجابات الاستبيان (مبدئي)
# ============================================
@router.post("/{survey_id}/submit")
def submit_answers(survey_id: int):
    return {"message": "Answers submitted successfully"}
