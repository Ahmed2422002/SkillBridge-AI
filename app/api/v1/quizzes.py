from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.quiz import Quiz
from app.models.question import Question
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuestionCreate,
    QuestionResponse,
)
from app.core.security import decode_access_token


router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


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
# 1. إنشاء اختبار جديد (POST)
# ============================================
@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz: QuizCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    new_quiz = Quiz(
        content_id=quiz.content_id,
        title=quiz.title,
        description=quiz.description,
        passing_score=quiz.passing_score,
        duration_minutes=quiz.duration_minutes,
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return new_quiz


# ============================================
# 2. جلب كل الاختبارات (GET)
# ============================================
@router.get("/", response_model=List[QuizResponse])
def get_quizzes(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    quizzes = db.query(Quiz).all()
    return quizzes


# ============================================
# 3. جلب اختبار واحد بالـ ID (GET)
# ============================================
@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return quiz


# ============================================
# 4. تحديث اختبار (PUT)
# ============================================
@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: int,
    quiz_data: QuizCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz.title = quiz_data.title
    quiz.description = quiz_data.description
    quiz.passing_score = quiz_data.passing_score
    quiz.duration_minutes = quiz_data.duration_minutes

    db.commit()
    db.refresh(quiz)
    return quiz


# ============================================
# 5. حذف اختبار (DELETE)
# ============================================
@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(quiz)
    db.commit()
    return {"message": "Quiz deleted successfully"}
    # ============================================
# 6. إضافة سؤال لاختبار (POST)
# ============================================
@router.post("/{quiz_id}/questions", response_model=QuestionResponse)
def add_question(
    quiz_id: int,
    question: QuestionCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    new_question = Question(
        quiz_id=quiz_id,
        question_text=question.question_text,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


# ============================================
# 7. جلب أسئلة اختبار (GET)
# ============================================
@router.get("/{quiz_id}/questions", response_model=List[QuestionResponse])
def get_questions(
    quiz_id: int,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)

    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    return questions


# ============================================
# 8. تقديم اختبار (POST) - مبدئي
# ============================================
@router.post("/submit")
def submit_quiz(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    return {"message": "Quiz submitted successfully"}