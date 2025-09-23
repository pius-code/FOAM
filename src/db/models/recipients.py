from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from src.db.models.base import Base
from sqlalchemy.dialects.postgresql import UUID as uuid
from sqlalchemy import func


class Recipient(Base):
    __tablename__ = "recipients"
    recipients_id = Column(
        uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    event_id = Column(uuid(as_uuid=True), ForeignKey("events.event_id"), nullable=False)
    recipients_name = Column(String(100), nullable=False)
    recipients_email = Column(String(255), unique=True, nullable=False, index=True)
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
