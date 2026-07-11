from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    slot_time: datetime


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    slot_time: datetime
    status: str
    cancel_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppointmentCancel(BaseModel):
    reason: str = Field(..., min_length=3, max_length=255)


class AppointmentReschedule(BaseModel):
    new_slot_time: datetime