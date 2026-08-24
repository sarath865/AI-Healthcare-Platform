from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return db.execute(statement).scalar_one_or_none()


def register_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
    role: UserRole = UserRole.PATIENT,
) -> User:

    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise ValueError("User with this email already exists")

    # Public registration must not create privileged accounts.
    if role != UserRole.PATIENT:
        role = UserRole.PATIENT

    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user