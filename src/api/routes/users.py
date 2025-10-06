from src.api.schema.user import UserCreate, UserResponse
from src.db.models.users import User
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.repository.user_repository import create_user
from src.core.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def Create_user(user_data: UserCreate, db: Session = Depends(get_db)) -> User:
    user = create_user(db, user_data)
    return UserResponse.model_validate(user, from_attributes=True)
