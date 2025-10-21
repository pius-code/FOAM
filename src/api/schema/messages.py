from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    message_body: str
    file_url: Optional[str] = None


class MessageResponse(BaseModel):
    message_id: UUID
    event_id: UUID
    message_body: str
    file_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        model_config = ConfigDict(from_attributes=True)
