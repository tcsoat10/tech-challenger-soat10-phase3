from datetime import datetime
from typing import Any, Dict, Type, TypeVar
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped

T = TypeVar("T", bound="BaseEntity")

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

    def to_json(self) -> Dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    @classmethod
    def from_json(cls: Type[T], json_data: Dict[str, Any]) -> T:
        return cls(**json_data)

__all__ = ["BaseEntity"]
