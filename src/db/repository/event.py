from sqlalchemy.orm import Session
from src.api.schema.event import EventCreate
from src.db.models.events import Event
from uuid import UUID


def create_event(db: Session, event: EventCreate, user_id: UUID):
    db_event = Event(
        user_id=user_id,
        event_name=event.event_name,
        event_type=event.event_type,
        event_description=event.event_description,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_Event_by_eventID(event_id: UUID, db: Session):
    return db.query(Event).filter(Event.event_id == event_id).first()
