from fastapi import APIRouter, HTTPException
from src.api.schema.event import EventResponse, EventCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from src.core.session import get_db
from src.db.repository.event import create_event
from src.db.repository.user_repository import get_user_id_by_email


router = APIRouter(prefix="/event", tags=["events"])


@router.post("/", response_model=EventResponse)
def Create_event(
    event_data: EventCreate, db: Session = Depends(get_db)
) -> EventResponse:
    user_id = get_user_id_by_email(db, event_data.user_email)
    if not user_id:
        raise HTTPException(status_code=404, details="User_id not found")
    event = create_event(db, event_data, user_id=user_id)
    return EventResponse.model_validate(event, from_attributes=True)
