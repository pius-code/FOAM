from fastapi import APIRouter, Depends, HTTPException
from src.api.schema.messages_scheduler import Scheduler_Create, Scheduler_Response
from src.core.session import get_db
from sqlalchemy.orm import Session
from src.db.repository.messages import get_messages_by_message_id
from src.db.repository.message_scheduler import create_message_schedule
from uuid import UUID

router = APIRouter(prefix="/message_scheduler/{message_id}", tags=["message_scheduler"])


@router.post("/", response_model=Scheduler_Response)
def create_message_scheduler(
    message_id: UUID,  # path param first
    message_schedule: Scheduler_Create,
    db: Session = Depends(get_db),
) -> Scheduler_Response:
    message = get_messages_by_message_id(db, message_id)
    if not message:
        raise HTTPException(
            status_code=404, detail="could not find message in the database"
        )
    created = create_message_schedule(db, message_schedule, message_id)
    return Scheduler_Response.model_validate(created, from_attributes=True)
