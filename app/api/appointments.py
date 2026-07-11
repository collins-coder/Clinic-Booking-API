from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services.booking_service import BookingService
from app.schemas.appointment import (AppointmentCancel, AppointmentReschedule)

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    try:
        return BookingService.book_appointment(
            db=db,
            doctor_id=appointment.doctor_id,
            patient_id=appointment.patient_id,
            slot_time=appointment.slot_time
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch(
    "/{appointment_id}/cancel",
    response_model=AppointmentResponse
)
def cancel_appointment(
    appointment_id: int,
    request: AppointmentCancel,
    db: Session = Depends(get_db)
):

    try:
        return BookingService.cancel_appointment(
            db,
            appointment_id,
            request.reason
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch(
    "/{appointment_id}/reschedule",
    response_model=AppointmentResponse
)
def reschedule_appointment(
    appointment_id: int,
    request: AppointmentReschedule,
    db: Session = Depends(get_db)
):

    try:
        return BookingService.reschedule_appointment(
            db,
            appointment_id,
            request.new_slot_time
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )