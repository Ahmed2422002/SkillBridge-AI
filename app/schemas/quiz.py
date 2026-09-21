from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ============================================
# مخططات الاختبار (Quiz)
# ============================================
class QuizCreate(BaseModel):
    content_id: int
    title: str
    description: Optional[str] = None
    passing_score: int = 70
    duration_minutes: int = 10


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    passing_score: Optional[int] = None
    duration_minutes: Optional[int] = None


class QuizResponse(BaseModel):
    id: int
    content_id: int
    title: str
    description: Optional[str] = None
    passing_score: int
    duration_minutes: int
    created_at: datetime   # ← التعديل هنا

    class Config:
        from_attributes = True


# ============================================
# مخططات الأسئلة (Question)
# ============================================
class QuestionCreate(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


# ============================================
# مخططات تسليم الاختبار
# ============================================
class QuizSubmit(BaseModel):
    quiz_id: int
    answers: dict  # {question_id: "A"}


class QuizResultResponse(BaseModel):
    quiz_id: int
    score: int
    passed: bool
    total_questions: int
    correct_answers: int
    wrong_answers: int
