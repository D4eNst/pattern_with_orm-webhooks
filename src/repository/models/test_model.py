from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


from repository.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now()
    )

    __mapper_args__ = {"eager_defaults": True}
