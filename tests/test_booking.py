from datetime import datetime, timedelta

from app.models.doctor import Doctor
from app.models.patient import Patient


def seed_data(db):

    timestamp = str(int(datetime.now().timestamp() * 1000000))

    doctor = Doctor(
        full_name=f"Dr Test {timestamp}",
        specialization="General",
        work_start=datetime.strptime("08:00", "%H:%M").time(),
        work_end=datetime.strptime("17:00", "%H:%M").time(),
    )

    patient = Patient(
        full_name=f"John Test {timestamp}",
        email=f"john{timestamp}@test.com",
        phone=f"07{timestamp[-8:]}"
    )

    db.add(doctor)
    db.add(patient)

    db.commit()
    db.refresh(doctor)
    db.refresh(patient)

    return doctor.id, patient.id


def test_successful_booking(client, db):

    doctor_id, patient_id = seed_data(db)

    slot = (
        datetime.now() + timedelta(days=1)
    ).replace(hour=10, minute=0, second=0, microsecond=0)

    response = client.post(
        "/appointments",
        json={
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "slot_time": slot.isoformat()
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["doctor_id"] == doctor_id
    assert body["patient_id"] == patient_id


def test_duplicate_booking(client, db):

    doctor_id, patient_id = seed_data(db)

    slot = (
        datetime.now() + timedelta(days=1)
    ).replace(hour=11, minute=0, second=0, microsecond=0)

    payload = {
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "slot_time": slot.isoformat()
    }

    first = client.post("/appointments", json=payload)

    assert first.status_code == 201

    second = client.post("/appointments", json=payload)

    assert second.status_code == 400
    assert "already been booked" in second.json()["detail"].lower()


def test_booking_in_the_past(client, db):

    doctor_id, patient_id = seed_data(db)

    slot = (
        datetime.now() - timedelta(days=1)
    ).replace(second=0, microsecond=0)

    response = client.post(
        "/appointments",
        json={
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "slot_time": slot.isoformat()
        }
    )

    assert response.status_code == 400
    assert "past" in response.json()["detail"].lower()


def test_booking_within_one_hour(client, db):

    doctor_id, patient_id = seed_data(db)

    slot = datetime.now() + timedelta(minutes=30)

    response = client.post(
        "/appointments",
        json={
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "slot_time": slot.isoformat()
        }
    )

    assert response.status_code == 400
    assert "one hour" in response.json()["detail"].lower()


def test_booking_outside_working_hours(client, db):

    doctor_id, patient_id = seed_data(db)

    slot = (
        datetime.now() + timedelta(days=1)
    ).replace(hour=20, minute=0, second=0, microsecond=0)

    response = client.post(
        "/appointments",
        json={
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "slot_time": slot.isoformat()
        }
    )

    assert response.status_code == 400
    assert "working hours" in response.json()["detail"].lower()