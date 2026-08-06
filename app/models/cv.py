from sqlalchemy import String, Text, Boolean, JSON, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import TimestampMixin
import datetime


class CV(TimestampMixin, Base):
    __tablename__ = "cvs"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(255), nullable=False)