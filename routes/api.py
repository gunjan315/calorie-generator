from fastapi import APIRouter
from config import settings
from routes import authentication, calories

api_router = APIRouter()

base_prefix = settings.version_prefix

api_router.include_router(
    authentication.router,
    prefix=f"{base_prefix}/auth",
    tags=["auth"],
)

api_router.include_router(
    calories.router,
    prefix=f"{base_prefix}/calories",
    tags=["calories"],
)