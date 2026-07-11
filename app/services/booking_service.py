from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment


class BookingService:

    @staticmethod
    def book_appointment(
        db: Session,
        doctor_id: int,
        patient_id: int,
        slot_time: datetime
    ):

        doctor = (
            db.query(Doctor)
            .filter(Doctor.id == doctor_id)
            .first()
        )

        if not doctor:
            raise ValueError("Doctor not found.")

        patient = (
            db.query(Patient)
            .filter(Patient.id == patient_id)
            .first()
        )

        if not patient:
            raise ValueError("Patient not found.")

        now = datetime.now(slot_time.tzinfo) 

        if slot_time <= now:
            raise ValueError("Cannot book an appointment in the past.")

    
        if slot_time < now + timedelta(hours=1):
            raise ValueError(
                "Appointments must be booked at least one hour in advance."
            )

        appointment_time = slot_time.time()

        if (
            appointment_time < doctor.work_start
            or appointment_time >= doctor.work_end
        ):
            raise ValueError(
                "Appointment is outside the doctor's working hours."
            )

        try:

            appointment = Appointment(
                doctor_id=doctor_id,
                patient_id=patient_id,
                slot_time=slot_time,
                status="BOOKED"
            )

            db.add(appointment)
            db.commit()
            db.refresh(appointment)

            return appointment

        except IntegrityError:
            db.rollback()
            raise ValueError("This appointment slot has already been booked.")

    @staticmethod
    def cancel_appointment(
        db: Session,
        appointment_id: int,
        reason: str
    ):

        appointment = (
            db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

        if not appointment:
            raise ValueError("Appointment not found.")

        if appointment.status == "CANCELLED":
            raise ValueError("Appointment has already been cancelled.")

        appointment.status = "CANCELLED"
        appointment.cancel_reason = reason

        db.commit()
        db.refresh(appointment)

        return appointment

    @staticmethod
    def reschedule_appointment(
        db: Session,
        appointment_id: int,
        new_slot_time: datetime
    ):

        appointment = (
            db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

        if not appointment:
            raise ValueError("Appointment not found.")

        if appointment.status == "CANCELLED":
            raise ValueError(
                "Cancelled appointments cannot be rescheduled."
            )

        doctor = (
            db.query(Doctor)
            .filter(Doctor.id == appointment.doctor_id)
            .first()
        )

        now = datetime.now(new_slot_time.tzinfo)  # Ensure timezone awareness

        if new_slot_time <= now:
            raise ValueError("Cannot reschedule to a past time.")

        if new_slot_time < now + timedelta(hours=1):
            raise ValueError(
                "Appointments must be scheduled at least one hour ahead."
            )

        appointment_time = new_slot_time.time()

        if (
            appointment_time < doctor.work_start
            or appointment_time >= doctor.work_end
        ):
            raise ValueError(
                "Selected slot is outside the doctor's working hours."
            )

        try:

            appointment.slot_time = new_slot_time

            db.commit()
            db.refresh(appointment)

            return appointment

        except IntegrityError:
            db.rollback()
            raise ValueError("Selected slot is already booked.")