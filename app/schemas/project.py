from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import re


class ProjectBase(BaseModel):
    title: str
    summary: str
    body: Optional[str] = None
    cover_image: Optional[str] = None
    images: list[str] = []
    tech_stack: list[str] = []
    tags: list[str] = []
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    paper_url: Optional[str] = None
    featured: bool = False
    published: bool = False
    sort_order: int = 0
    # Structured sections
    overview: Optional[str] = None
    dataset: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    challenges: Optional[str] = None


class ProjectCreate(ProjectBase):
    slug: Optional[str] = None

    @field_validator("slug", mode="before")
    @classmethod
    def auto_slug(cls, v, info):
        if v:
            return v
        title = info.data.get("title", "")
        return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    body: Optional[str] = None
    cover_image: Optional[str] = None
    images: Optional[list[str]] = None
    tech_stack: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    paper_url: Optional[str] = None
    featured: Optional[bool] = None
    published: Optional[bool] = None
    sort_order: Optional[int] = None
    # Structured sections
    overview: Optional[str] = None
    dataset: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    challenges: Optional[str] = None


class ProjectOut(ProjectBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}