from datetime import datetime

from sqlalchemy import String, DateTime, FetchedValue
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from repository.base import Base


class Test(Base):  # type: ignore
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    text: Mapped[str] = mapped_column(String(length=64), nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_onupdate=FetchedValue(for_update=True),
    )

    __mapper_args__ = {"eager_defaults": True}
