from pydantic import BaseModel, ConfigDict
from uuid import UUID
from src.enums.event import EventType
from datetime import datetime
from pydantic import EmailStr


class EventCreate(BaseModel):
    user_email: EmailStr
    event_name: str
    event_type: EventType
    event_description: str


class EventResponse(BaseModel):
    event_id: UUID
    user_id: UUID
    event_name: str
    event_type: EventType
    event_description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = ConfigDict(from_attributes=True)
