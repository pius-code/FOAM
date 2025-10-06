from sqlalchemy import Column, String, DateTime, func, ForeignKey, Text
from src.db.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Message(Base):
    __tablename__ = "messages"
    message_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.event_id"), nullable=False)
    message_body = Column(Text, nullable=False)
    file_url = Column(String(255), nullable=True)
    created_at = Column(
        DateTime, server_default=func.timezone("UTC", func.now()), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
        nullable=False,
    )
