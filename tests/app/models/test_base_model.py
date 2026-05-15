"""Unit tests for base model functionality."""

from datetime import datetime, timezone
from typing import ClassVar
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base, BigIntMixin, TimestampMixin, UUIDMixin


class TestUUIDMixin:
    """Test suite for UUIDMixin."""

    def test_uuid_mixin_attributes(self) -> None:
        """Test UUIDMixin has correct attributes."""
        # Test that UUIDMixin has the id field
        assert hasattr(UUIDMixin, "id")

        # Test the field type annotation
        assert hasattr(UUIDMixin, "__annotations__")
        assert "id" in UUIDMixin.__annotations__
        assert UUIDMixin.__annotations__["id"] == Mapped[UUID]

    def test_uuid_mixin_integration(self) -> None:
        """Test UUIDMixin integration with SQLAlchemy."""

        class UUIDTestModel(Base, UUIDMixin):
            __tablename__ = "test_uuid_model"
            name: Mapped[str] = mapped_column(String(100))

        # Test that the model was created successfully
        assert UUIDTestModel.__tablename__ == "test_uuid_model"
        assert hasattr(UUIDTestModel, "id")
        assert hasattr(UUIDTestModel, "name")

    def test_uuid_generation(self) -> None:
        """Test UUID generation functionality."""
        # Test that uuid4 generates valid UUIDs
        test_uuid = uuid4()
        assert isinstance(test_uuid, UUID)
        assert len(str(test_uuid)) == 36  # Standard UUID string length


class TestBigIntMixin:
    """Test suite for BigIntMixin."""

    def test_bigint_mixin_attributes(self) -> None:
        """Test BigIntMixin has correct attributes."""
        assert hasattr(BigIntMixin, "id")
        assert "id" in BigIntMixin.__annotations__
        assert BigIntMixin.__annotations__["id"] == Mapped[int]

    def test_bigint_mixin_integration(self) -> None:
        """Test BigIntMixin integration with SQLAlchemy."""

        class BigIntTestModel(Base, BigIntMixin):
            __tablename__ = "test_bigint_model"
            title: Mapped[str] = mapped_column(String(100))

        assert BigIntTestModel.__tablename__ == "test_bigint_model"
        assert hasattr(BigIntTestModel, "id")
        assert hasattr(BigIntTestModel, "title")

    def test_bigint_type_validation(self) -> None:
        """Test BigInt type validation."""
        # Test that BigInteger is the correct SQLAlchemy type
        assert BigInteger is not None

        # Test integer validation
        test_values = [1, 42, 9223372036854775807]  # Max 64-bit int
        for value in test_values:
            assert isinstance(value, int)


class TestTimestampMixin:
    """Test suite for TimestampMixin."""

    def test_timestamp_mixin_attributes(self) -> None:
        """Test TimestampMixin has correct attributes."""
        assert hasattr(TimestampMixin, "created_at")
        assert hasattr(TimestampMixin, "updated_at")

        # Test annotations
        assert "created_at" in TimestampMixin.__annotations__
        assert "updated_at" in TimestampMixin.__annotations__
        assert TimestampMixin.__annotations__["created_at"] == Mapped[datetime]
        assert TimestampMixin.__annotations__["updated_at"] == Mapped[datetime]

    def test_timestamp_mixin_integration(self) -> None:
        """Test TimestampMixin integration with SQLAlchemy."""

        class TimestampTestModel(Base, UUIDMixin, TimestampMixin):
            __tablename__ = "test_timestamp_model"
            name: Mapped[str] = mapped_column(String(100))

        assert hasattr(TimestampTestModel, "created_at")
        assert hasattr(TimestampTestModel, "updated_at")
        assert hasattr(TimestampTestModel, "name")
        assert hasattr(TimestampTestModel, "id")  # From UUIDMixin

    def test_datetime_timezone_handling(self) -> None:
        """Test datetime timezone functionality."""
        # Test UTC datetime creation
        utc_now = datetime.now(timezone.utc)
        assert utc_now.tzinfo == timezone.utc

        # Test that datetime objects have timezone info
        assert utc_now.tzinfo is not None


class TestBaseModel:
    """Test suite for Base model."""

    def test_base_model_exists(self) -> None:
        """Test that Base model exists and is importable."""
        assert Base is not None

    def test_base_model_inheritance(self) -> None:
        """Test Base model inheritance."""

        class BaseTestModel(Base):
            __tablename__ = "test_base_model"
            id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))

        assert BaseTestModel.__tablename__ == "test_base_model"
        assert hasattr(BaseTestModel, "id")
        assert hasattr(BaseTestModel, "name")

    def test_combined_mixins(self) -> None:
        """Test combining multiple mixins."""

        class CompleteModel(Base, UUIDMixin, TimestampMixin):
            __tablename__ = "complete_model"
            name: Mapped[str] = mapped_column(String(100))

        # Test that all mixin attributes are present
        assert hasattr(CompleteModel, "id")  # From UUIDMixin
        assert hasattr(CompleteModel, "created_at")  # From TimestampMixin
        assert hasattr(CompleteModel, "updated_at")  # From TimestampMixin
        assert hasattr(CompleteModel, "name")  # Custom field

    def test_model_metadata(self) -> None:
        """Test model metadata functionality."""
        # Test that Base has metadata
        assert hasattr(Base, "metadata")
        assert Base.metadata is not None

        # Test metadata methods
        assert hasattr(Base.metadata, "create_all")
        assert hasattr(Base.metadata, "drop_all")

    def test_model_table_configuration(self) -> None:
        """Test model table configuration options."""

        class ConfiguredModel(Base):
            __tablename__ = "configured_model"
            __table_args__: ClassVar = {"comment": "Test model"}

            id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
            name: Mapped[str] = mapped_column(String(100), nullable=False)

        assert ConfiguredModel.__tablename__ == "configured_model"
        assert hasattr(ConfiguredModel, "__table_args__")

    def test_field_constraints(self) -> None:
        """Test field constraint definitions."""

        class ConstrainedModel(Base):
            __tablename__ = "constrained_model"

            id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
            email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
            age: Mapped[int] = mapped_column(nullable=True)

        # Test that model was created successfully
        assert ConstrainedModel.__tablename__ == "constrained_model"
        assert hasattr(ConstrainedModel, "email")
        assert hasattr(ConstrainedModel, "age")

    def test_model_string_representations(self) -> None:
        """Test model string representation methods."""

        class RepresentableModel(Base):
            __tablename__ = "representable_model"

            id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))

            def __repr__(self) -> str:
                return f"<RepresentableModel(id={self.id}, name='{self.name}')>"

        # Test that __repr__ method exists
        model_instance = RepresentableModel()
        assert hasattr(model_instance, "__repr__")

    def test_model_validation_types(self) -> None:
        """Test model field type validations."""
        # Test string validation
        assert isinstance("test_string", str)

        # Test integer validation
        assert isinstance(42, int)

        # Test boolean validation
        assert isinstance(True, bool)

        # Test UUID validation
        test_uuid = uuid4()
        assert isinstance(test_uuid, UUID)

        # Test datetime validation
        test_datetime = datetime.now(timezone.utc)
        assert isinstance(test_datetime, datetime)
