from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    func,
    DateTime,
)
from src.db.models.base import Base
from sqlalchemy.dialects.postgresql import UUID as uuid


class Message_scheduler(Base):
    __tablename__ = "messages_scheduler"
    messages_scheduler_id = Column(
        uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    message_id = Column(
        uuid(as_uuid=True), ForeignKey("messages.message_id"), nullable=False
    )
    frequency_type = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime, server_default=func.timezone("UTC", func.now()), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
        nullable=False,
    )
