from datetime import time, datetime
from pydantic import BaseModel


class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    work_start: time
    work_end: time


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True