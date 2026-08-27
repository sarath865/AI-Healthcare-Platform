from sqlalchemy.orm import Session

from app.models.hospital import Hospital
from app.models.user import User, UserRole
from app.repositories.hospital_repository import (
    create_hospital,
    delete_hospital,
    get_hospital_by_id,
    get_hospital_by_registration_number,
    get_hospitals,
    update_hospital,
)
from app.schemas.hospital import HospitalCreate, HospitalUpdate


def create_hospital_service(
    db: Session,
    hospital_data: HospitalCreate,
    current_user: User,
) -> Hospital:

    if current_user.role not in {
        UserRole.SUPER_ADMIN,
        UserRole.HOSPITAL_ADMIN,
    }:
        raise PermissionError(
            "Only super admins and hospital admins can create hospitals"
        )

    existing = get_hospital_by_registration_number(
        db,
        hospital_data.registration_number,
    )

    if existing:
        raise ValueError(
            "Hospital registration number already exists"
        )

    hospital = Hospital(
        name=hospital_data.name,
        registration_number=hospital_data.registration_number,
        address=hospital_data.address,
        phone=hospital_data.phone,
        email=hospital_data.email,
    )

    return create_hospital(db, hospital)


def get_hospital_service(
    db: Session,
    hospital_id: int,
) -> Hospital:

    hospital = get_hospital_by_id(
        db,
        hospital_id,
    )

    if not hospital:
        raise ValueError("Hospital not found")

    return hospital


def get_all_hospitals_service(
    db: Session,
) -> list[Hospital]:

    return get_hospitals(db)


def update_hospital_service(
    db: Session,
    hospital_id: int,
    hospital_data: HospitalUpdate,
    current_user: User,
) -> Hospital:

    if current_user.role not in {
        UserRole.SUPER_ADMIN,
        UserRole.HOSPITAL_ADMIN,
    }:
        raise PermissionError(
            "Only super admins and hospital admins can update hospitals"
        )

    hospital = get_hospital_by_id(
        db,
        hospital_id,
    )

    if not hospital:
        raise ValueError("Hospital not found")

    update_data = hospital_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(hospital, field, value)

    return update_hospital(db, hospital)


def delete_hospital_service(
    db: Session,
    hospital_id: int,
    current_user: User,
) -> None:

    if current_user.role not in {
        UserRole.SUPER_ADMIN,
        UserRole.HOSPITAL_ADMIN,
    }:
        raise PermissionError(
            "Only super admins and hospital admins can delete hospitals"
        )

    hospital = get_hospital_by_id(
        db,
        hospital_id,
    )

    if not hospital:
        raise ValueError("Hospital not found")

    delete_hospital(db, hospital)