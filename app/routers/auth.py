from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.schemas.auth import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        user = register_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            role=user_data.role,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        subject=str(user.id),
        role=user.role.value,
    )

    refresh_token = create_refresh_token(
        subject=str(user.id),
        role=user.role.value,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )