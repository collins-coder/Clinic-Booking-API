from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.utils.slots import generate_slots

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.get("/{doctor_id}/availability")
def doctor_availability(
    doctor_id: int,
    appointment_date: date = Query(...),
    db: Session = Depends(get_db)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found."
        )

    all_slots = generate_slots(
        doctor.work_start,
        doctor.work_end,
        appointment_date
    )

    booked_slots = (
        db.query(Appointment.slot_time)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == "BOOKED",
            Appointment.slot_time >= all_slots[0],
            Appointment.slot_time < all_slots[-1]
        )
        .all()
    )

    booked = {slot.slot_time for slot in booked_slots}

    available = [
        slot for slot in all_slots
        if slot not in booked
    ]

    return {
        "doctor_id": doctor.id,
        "doctor_name": doctor.full_name,
        "date": appointment_date,
        "available_slots": available
    }