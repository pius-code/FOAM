from fastapi import APIRouter, Depends, HTTPException
from src.api.schema.messages import MessageResponse, MessageCreate
from uuid import UUID
from src.core.session import get_db
from sqlalchemy.orm import Session
from src.db.repository.event import get_Event_by_eventID
from src.db.repository.messages import create_message


router = APIRouter(prefix="/event/{event_id}/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse)
def create_event_message(
    message: MessageCreate, event_id: UUID, db: Session = Depends(get_db)
) -> MessageResponse:
    event = get_Event_by_eventID(event_id, db)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    msg = create_message(db, message=message, event_id=event_id)
    return MessageResponse.model_validate(msg, from_attributes=True)
