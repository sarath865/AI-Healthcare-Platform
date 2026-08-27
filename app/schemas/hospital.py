from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class HospitalCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    registration_number: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    address: str = Field(
        ...,
        min_length=5,
        max_length=500,
    )

    phone: str = Field(
        ...,
        min_length=7,
        max_length=20,
    )

    email: EmailStr


class HospitalUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    address: str | None = Field(
        default=None,
        min_length=5,
        max_length=500,
    )

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    email: EmailStr | None = None

    is_active: bool | None = None


class HospitalResponse(BaseModel):
    id: int
    name: str
    registration_number: str
    address: str
    phone: str
    email: EmailStr
    admin_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }