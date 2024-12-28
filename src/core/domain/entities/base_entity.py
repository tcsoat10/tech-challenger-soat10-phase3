from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped


class BaseEntity(DeclarativeBase):
    """
    Base class for all entities in the application.

    This abstract class provides common fields such as ID, timestamps for creation and updates.
    All other database models should inherit from this base class.
    """

    __abstract__ = True

    # Primary Key: Auto-incrementing integer ID
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Timestamp: Record creation time (default: current UTC time)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Timestamp: Record last update time (auto-updated on modification)
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Timestamp: Record inactivation time
    inactivated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=True
    )

__all__ = ["BaseEntity"]
