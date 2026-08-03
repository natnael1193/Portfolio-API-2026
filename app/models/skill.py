from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import TimestampMixin


class Skill(TimestampMixin, Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "ML", "Backend", "Tools"
    level: Mapped[int] = mapped_column(Integer, default=3)              # 1–5
    icon: Mapped[str] = mapped_column(String(100), nullable=True)       # devicon class or URL
    sort_order: Mapped[int] = mapped_column(default=0)
