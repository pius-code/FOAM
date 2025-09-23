from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID as uuid
from sqlalchemy import func

from src.db.models.base import Base


class Event(Base):
    __tablename__ = "events"
    event_id = Column(
        uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    user_id = Column(
        uuid(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True
    )
    event_name = Column(String(255), nullable=False)
    event_type = Column(String(100), nullable=False)
    event_description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime, server_default=func.timezone("UTC", func.now()), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
        nullable=False,
    )
