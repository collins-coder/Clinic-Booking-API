from datetime import datetime, timedelta

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment


def seed_data(db):

    doctor = Doctor(
        full_name="Availability Doctor",
        specialization="General",
        work_start=datetime.strptime("08:00", "%H:%M").time(),
        work_end=datetime.strptime("17:00", "%H:%M").time(),
    )

    patient = Patient(
        full_name="Availability Patient",
        email=f"availability{int(datetime.now().timestamp()*1000000)}@test.com",
        phone="0712345678",
    )

    db.add(doctor)
    db.add(patient)

    db.commit()
    db.refresh(doctor)
    db.refresh(patient)

    return doctor, patient


def test_doctor_availability(client, db):

    doctor, patient = seed_data(db)

    date = (datetime.now() + timedelta(days=1)).date()

    response = client.get(
        f"/doctors/{doctor.id}/availability",
        params={"date": date.isoformat()}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["doctor_id"] == doctor.id
    assert len(body["available_slots"]) > 0


def test_booked_slot_removed_from_availability(client, db):

    doctor, patient = seed_data(db)

    slot = (
        datetime.now() + timedelta(days=1)
    ).replace(hour=10, minute=0, second=0, microsecond=0)

    appointment = Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        slot_time=slot,
        status="BOOKED"
    )

    db.add(appointment)
    db.commit()

    response = client.get(
        f"/doctors/{doctor.id}/availability",
        params={"date": slot.date().isoformat()}
    )

    assert response.status_code == 200

    body = response.json()

    assert slot.isoformat() not in body["available_slots"]