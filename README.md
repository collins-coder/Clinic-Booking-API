Clinic Booking API
A RESTful backend API built with FastAPI, SQLAlchemy, MySQL and Alembic for managing doctor appointments. The API allows patients to book appointments, check doctor availability, cancel appointments, and reschedule appointments while enforcing business rules and preventing double bookings.

Technology Stack
•	Python 3.13
•	FastAPI
•	SQLAlchemy ORM
•	MySQL
•	Alembic
•	Pydantic
•	Pytest
•	Uvicorn

Project Structure
clinic-booking-api/
│
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── seed.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_booking.py
│   └── test_availability.py
│
├── requirements.txt
├── alembic.ini
├── .env
└── README.md

Features
•	Book appointments
•	View doctor availability
•	Cancel appointments
•	Reschedule appointments
•	View patient appointments
•	Input validation
•	Business rule validation
•	Automated tests
•	Database migrations

Business Rules
The application enforces the following rules:
•	A patient cannot book an appointment in the past.
•	Appointments must be booked at least one hour in advance.
•	Appointments must be within the doctor's working hours.
•	A doctor cannot have two appointments at the same date and time.
•	Cancelled appointments cannot be rescheduled.
•	Only available appointment slots are returned when checking availability.

Database Design
The application consists of three primary entities:


Doctor
Stores doctor information including:
•	Full Name
•	Specialization
•	Working Start Time
•	Working End Time
Patient
Stores patient information including:
•	Full Name
•	Email
•	Phone Number
Appointment
Stores booking information including:
•	Doctor
•	Patient
•	Appointment Date & Time
•	Status
•	Cancellation Reason
Relationships:
•	One Doctor → Many Appointments
•	One Patient → Many Appointments

Concurrency Handling
The system prevents double booking using a database-level unique constraint on:
(doctor_id, slot_time)
This guarantees that only one appointment can exist for a doctor at a specific time, even if multiple booking requests arrive simultaneously.
The application catches database IntegrityError exceptions and returns a meaningful error response instead of exposing database errors.

API Endpoints
Appointments
Method	Endpoint	Description
POST	/appointments	Book appointment
PATCH	/appointments/{id}/cancel	Cancel appointment
PATCH	/appointments/{id}/reschedule	Reschedule appointment
Doctors
Method	Endpoint	Description
GET	/doctors/{id}/availability	View available slots
Patients
Method	Endpoint	Description
GET	/patients/{id}/appointments	View patient appointments

Installation
Clone the repository.
git clone <https://github.com/collins-coder/Clinic-Booking-API.git>
Navigate to the project.
cd clinic-booking-api
Create a virtual environment.
python -m venv venv
Activate the environment.
Windows
venv\Scripts\activate
Install dependencies.
pip install -r requirements.txt

Environment Variables
Create a .env file.
Example:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/clinic_booking

SECRET_KEY=your_secret_key

ALGORITHM=HS256

Database Migration
Run migrations.
alembic upgrade head

Seed Sample Data
python -m app.seed

Run the Application
uvicorn app.main:app --reload
Swagger Documentation:
http://127.0.0.1:8000/docs
ReDoc:
http://127.0.0.1:8000/redoc
Running Tests
Run all tests.
pytest -v
Generate coverage report.
pytest --cov=app --cov-report=term-missing

Design Decisions
Several design decisions were made during development:
•	FastAPI was chosen for its high performance and automatic OpenAPI documentation.
•	SQLAlchemy ORM was used to simplify database interactions.
•	Alembic manages database schema migrations.
•	Business logic was separated into a service layer to keep API routes lightweight.
•	Validation is performed before persisting data.
•	Database constraints are used to guarantee data integrity.

Assumptions
•	Appointment duration is 30 minutes.
•	Doctors work fixed daily schedules.
•	Appointment slots cannot overlap.
•	Only active appointments affect availability.
•	All timestamps are handled consistently by the application.



Future Improvements
Possible enhancements include:
•	JWT Authentication
•	User Roles (Admin, Doctor, Patient)
•	Email Notifications
•	SMS Appointment Reminders
•	Calendar Integration
•	Doctor Leave Management
•	Pagination and Filtering
•	Docker Deployment
•	CI/CD Pipeline

Author
Developed as part of a backend engineering technical assessment using FastAPI, SQLAlchemy, MySQL, Alembic, and Pytest.

