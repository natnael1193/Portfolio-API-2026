from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SkillBase(BaseModel):
    name: str
    category: str
    level: int = 3
    icon: Optional[str] = None
    sort_order: int = 0


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    level: Optional[int] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None


class SkillOut(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
