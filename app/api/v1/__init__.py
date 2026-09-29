from fastapi import APIRouter
from . import auth, users, mentors, quizzes, progress, roadmaps, survey, admin, videos

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(mentors.router)
api_router.include_router(quizzes.router)
api_router.include_router(progress.router)
api_router.include_router(roadmaps.router)  # لاحظ: roadmaps (بالجمع)
api_router.include_router(survey.router)
api_router.include_router(admin.router)
api_router.include_router(videos.router)
