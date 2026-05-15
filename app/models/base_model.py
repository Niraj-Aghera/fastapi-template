"""Base model definitions for SQLAlchemy ORM classes.

This module provides base model classes with common functionality like:
- A declarative base for all models to inherit from.
- Mixins for common column types like UUID/BigInt primary keys and timestamps.
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass

class UUIDMixin:
    """Mixin to add a UUID primary key column."""

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True,
        default=uuid4,
        server_default=text("gen_random_uuid()"),
    )

class BigIntMixin:
    """Mixin to add a BigInt auto-incrementing primary key column."""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
        server_onupdate=func.now(),
        nullable=False,
    )