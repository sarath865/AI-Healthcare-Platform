from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    HOSPITAL_ADMIN = "hospital_admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    PHARMACIST = "pharmacist"
    LAB_TECHNICIAN = "lab_technician"
    RECEPTIONIST = "receptionist"
    PATIENT = "patient"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.PATIENT,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )