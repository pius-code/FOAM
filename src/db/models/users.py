from sqlalchemy import Column, String
from src.db.models.base import Base
from sqlalchemy.dialects.postgresql import UUID as uuid
from sqlalchemy import DateTime
from sqlalchemy import func


class User(Base):
    __tablename__ = "users"
    user_id = Column(
        uuid(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    username = Column(String(50), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(
        DateTime, server_default=func.timezone("UTC", func.now()), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
        nullable=False,
    )
