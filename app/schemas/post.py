from pydantic import BaseModel, field_validator
from datetime import datetime, date
from typing import Optional
import re


class PostBase(BaseModel):
    title: str
    summary: str
    body: Optional[str] = None
    cover_image: Optional[str] = None
    tags: list[str] = []
    reading_time: int = 0
    published: bool = False
    published_at: Optional[date] = None


class PostCreate(PostBase):
    slug: Optional[str] = None

    @field_validator("slug", mode="before")
    @classmethod
    def auto_slug(cls, v, info):
        if v:
            return v
        title = info.data.get("title", "")
        return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


class PostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    body: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[list[str]] = None
    reading_time: Optional[int] = None
    published: Optional[bool] = None
    published_at: Optional[date] = None


class PostOut(PostBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
