from src.api.routes.users import router as user_router
from src.api.routes.event import router as event_router
from src.api.routes.message import router as messages_router

from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(event_router)
api_router.include_router(messages_router)
