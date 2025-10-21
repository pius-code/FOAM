from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID


class Scheduler_Create(BaseModel):
    frequency_type: str
    start_date: datetime
    end_date: Optional[datetime] = None


class Scheduler_Response(BaseModel):
    message_scheduler_id: UUID
    message_id: UUID
    frequency_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
