from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )