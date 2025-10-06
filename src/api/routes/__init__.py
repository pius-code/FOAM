from src.api.routes.users import router as user_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user_router)
