from sqlalchemy import String, Text, Boolean, JSON, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import TimestampMixin
import datetime


class Post(TimestampMixin, Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=True)           # MDX content
    cover_image: Mapped[str] = mapped_column(String(500), nullable=True)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    reading_time: Mapped[int] = mapped_column(default=0)             # minutes
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime.date] = mapped_column(Date, nullable=True)
