from fastapi import FastAPI

from app.core.config import settings
from app.routers.auth import router as auth_router
from app.routers.rbac import router as rbac_router
from app.routers.hospitals import router as hospital_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(rbac_router)
app.include_router(hospital_router)


@app.get("/")
def root():
    return {
        "message": "AI Healthcare Platform API",
        "status": "running",
    }