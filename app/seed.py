from datetime import time

from app.core.database import SessionLocal
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment


db = SessionLocal()

if db.query(Doctor).count() == 0:

    doctors = [

        Doctor(
            full_name="Dr. John Kariuki",
            specialization="General Medicine",
            work_start=time(8, 0),
            work_end=time(17, 0),
        ),

        Doctor(
            full_name="Dr. Sarah Kemboi",
            specialization="Pediatrics",
            work_start=time(8, 0),
            work_end=time(17, 0),
        ),

        Doctor(
            full_name="Dr. David Ojwang",
            specialization="Dermatology",
            work_start=time(9, 0),
            work_end=time(16, 0),
        ),

        Doctor(
            full_name="Dr. Grace Muthuku",
            specialization="Cardiology",
            work_start=time(8, 30),
            work_end=time(16, 30),
        ),

        Doctor(
            full_name="Dr. Collins White",
            specialization="Orthopedics",
            work_start=time(8, 0),
            work_end=time(15, 30),
        ),
    ]

    db.add_all(doctors)


if db.query(Patient).count() == 0:

    patients = [

        Patient(
            full_name="Alice Johnson",
            email="alice@yahoo.com",
            phone="0712345678"
        ),

        Patient(
            full_name="Brian Otieno",
            email="brian@mail.com",
            phone="0723456789"
        ),

        Patient(
            full_name="Carol Wanjiku",
            email="carol@gmail.com",
            phone="0734567890"
        ),
    ]

    db.add_all(patients)

db.commit()
db.close()

print("Database seeded successfully.")