from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class CVBase(BaseModel):
    link: str


class CVCreate(CVBase):
    pass


class CVUpdate(BaseModel):
    link: Optional[str] = None


class CVOut(CVBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}    
