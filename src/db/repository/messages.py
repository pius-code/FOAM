from sqlalchemy.orm import Session
from src.api.schema.messages import MessageCreate
from uuid import UUID
from src.db.models.messages import Message


def create_message(db: Session, message: MessageCreate, event_id: UUID):
    db_message = Message(
        event_id=event_id, message_body=message.message_body, file_url=message.file_url
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
