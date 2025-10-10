from sqlalchemy.orm import Session
from src.db.models.users import User
from src.api.schema.user import UserCreate
from pydantic import EmailStr
from uuid import UUID


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    return db_user


def get_user_by_email(db: Session, email: EmailStr) -> User:
    """Get a user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User:
    """Get a user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, id) -> User:
    """Get a user by id"""
    return db.query(User).filter(User.id == id).first()


def get_user_id_by_email(db: Session, email: EmailStr) -> UUID | None:
    """Return the user ID given their email, or None if not found."""
    user = get_user_by_email(db, email)
    if user:
        return user.id
    return None
