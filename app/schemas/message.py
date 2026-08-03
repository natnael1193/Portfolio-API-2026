from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    body: str


class MessageOut(BaseModel):
    id: int
    name: str
    email: str
    subject: Optional[str]
    body: str
    read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
