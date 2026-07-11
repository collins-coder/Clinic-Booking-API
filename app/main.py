from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.appointments import router as appointment_router
from app.api.doctors import router as doctor_router

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.api.patients import router as patient_router


app = FastAPI(
    title="Clinic Booking API",
    version="1.0.0",
    description="Savannah Informatics Backend Assessment"
)

app.include_router(appointment_router)
app.include_router(doctor_router)
app.include_router(patient_router)
@app.get("/")
def root():
    return {
        "message": "Clinic Booking API is running successfully."
    }