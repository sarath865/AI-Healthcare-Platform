from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hospital import Hospital


def create_hospital(
    db: Session,
    hospital: Hospital,
) -> Hospital:
    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    return hospital


def get_hospital_by_id(
    db: Session,
    hospital_id: int,
) -> Hospital | None:
    statement = select(Hospital).where(
        Hospital.id == hospital_id
    )

    return db.execute(statement).scalar_one_or_none()


def get_hospital_by_registration_number(
    db: Session,
    registration_number: str,
) -> Hospital | None:
    statement = select(Hospital).where(
        Hospital.registration_number
        == registration_number
    )

    return db.execute(statement).scalar_one_or_none()


def get_hospitals(
    db: Session,
) -> list[Hospital]:
    statement = select(Hospital).order_by(
        Hospital.id.desc()
    )

    return list(
        db.execute(statement).scalars().all()
    )


def update_hospital(
    db: Session,
    hospital: Hospital,
) -> Hospital:
    db.commit()
    db.refresh(hospital)

    return hospital


def delete_hospital(
    db: Session,
    hospital: Hospital,
) -> None:
    db.delete(hospital)
    db.commit()