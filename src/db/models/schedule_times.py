from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, Time, Date
from src.db.models.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Schedule_times(Base):
    __tablename__ = "schedule_times"
    schedule_times_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    message_scheduler_id = Column(
        UUID(as_uuid=True),
        ForeignKey("messages_scheduler.messages_scheduler_id"),
        nullable=False,
    )
    send_time = Column(Time, nullable=False)
    day_of_week = Column(Integer, nullable=True)
    week_of_month = Column(Integer, nullable=True)
    day_of_month = Column(Integer, nullable=True)
    month_of_year = Column(Integer, nullable=True)
    specific_date = Column(Date, nullable=True)
    created_at = Column(
        DateTime, server_default=func.timezone("UTC", func.now()), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=func.timezone("UTC", func.now()),
        onupdate=func.timezone("UTC", func.now()),
        nullable=False,
    )
