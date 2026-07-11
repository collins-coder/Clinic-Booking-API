from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.patient import Patient
from app.models.appointment import Appointment

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.get("/{patient_id}/appointments")
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == patient_id,
            Appointment.status == "BOOKED",
            Appointment.slot_time >= datetime.now()
        )
        .order_by(Appointment.slot_time.asc())
        .all()
    )

    return {
        "patient_id": patient.id,
        "patient_name": patient.full_name,
        "appointments": appointments
    }