from sqlalchemy.orm import Session
from src.db.models.messages_scheduler import Message_scheduler
from src.api.schema.messages_scheduler import Scheduler_Create
from uuid import UUID


def create_message_schedule(
    db: Session, message_schedule: Scheduler_Create, message_id: UUID
) -> Message_scheduler:
    db_message_scheduler = Message_scheduler(
        message_id=message_id,
        frequency_type=message_schedule.frequency_type,
        start_date=message_schedule.start_date,
        end_date=message_schedule.end_date,
    )
    db.add(db_message_scheduler)
    db.commit()
    db.refresh(db_message_scheduler)
    return db_message_scheduler
