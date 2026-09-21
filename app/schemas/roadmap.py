from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RoadmapCreate(BaseModel):
    title: str
    description: Optional[str] = None
    goal: str
    level: str
    steps: List[str]


class RoadmapUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    goal: Optional[str] = None
    level: Optional[str] = None
    steps: Optional[List[str]] = None
    progress: Optional[int] = None
    is_completed: Optional[int] = None


class RoadmapResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    goal: str
    level: str
    steps: List[str]
    progress: int
    is_completed: int
    created_at: datetime

    class Config:
        from_attributes = True
