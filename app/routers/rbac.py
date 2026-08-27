from fastapi import APIRouter, Depends

from app.core.permissions import require_roles
from app.models.user import User, UserRole


router = APIRouter(
    prefix="/rbac",
    tags=["RBAC"],
)


@router.get("/patient-only")
def patient_only(
    current_user: User = Depends(
        require_roles(UserRole.PATIENT)
    ),
):
    return {
        "message": "Patient access granted",
        "user": current_user.email,
        "role": current_user.role.value,
    }


@router.get("/doctor-only")
def doctor_only(
    current_user: User = Depends(
        require_roles(UserRole.DOCTOR)
    ),
):
    return {
        "message": "Doctor access granted",
        "user": current_user.email,
        "role": current_user.role.value,
    }


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.HOSPITAL_ADMIN,
        )
    ),
):
    return {
        "message": "Admin access granted",
        "user": current_user.email,
        "role": current_user.role.value,
    }