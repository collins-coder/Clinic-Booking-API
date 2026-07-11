from datetime import datetime
from pydantic import BaseModel, EmailStr


class PatientBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True