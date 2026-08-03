from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class ExperienceBase(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    current: bool = False
    description: Optional[str] = None
    bullets: list[str] = []
    tech_used: list[str] = []
    sort_order: int = 0


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    current: Optional[bool] = None
    description: Optional[str] = None
    bullets: Optional[list[str]] = None
    tech_used: Optional[list[str]] = None
    sort_order: Optional[int] = None


class ExperienceOut(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
