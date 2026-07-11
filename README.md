 Clinic Booking API
A RESTful Clinic Booking API built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Alembic**. The system allows patients to book appointments, view doctor availability, cancel appointments, and reschedule appointments while enforcing business rules and preventing double bookings.

# Live Deployment
**Base URL**

https://clinic-booking-api-opnl.onrender.com/

**Swagger Documentation**

https://clinic-booking-api-opnl.onrender.com/docs

**ReDoc Documentation**

https://clinic-booking-api-opnl.onrender.com/redoc

# Technology Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest
- Uvicorn
- Render

# System Architecture

The application follows a layered architecture to separate responsibilities.

Client
   │
   ▼
FastAPI Routes
   │
   ▼
Service Layer
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PostgreSQL Database
```

## Components

### API Layer

Responsible for:

- Receiving HTTP requests
- Request validation
- Returning HTTP responses
- Calling the appropriate service methods

### Service Layer

Contains all business logic including:

- Booking appointments
- Validation
- Availability calculation
- Cancellation
- Rescheduling

### Database Layer

Responsible for:

- Persisting data
- Managing relationships
- Enforcing constraints



# Project Structure

clinic-booking-api/
│
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── seed.py
│   └── main.py
│
├── tests/
│
├── requirements.txt
├── alembic.ini
├── README.md
└── .env



# Database Models

## Doctor
Stores:
- Full name
- Specialization
- Working start time
- Working end time

Relationship

Doctor
   │
   └──────< Appointment


## Patient

Stores:

- Full name
- Email
- Phone number

Relationship

Patient
    │
    └──────< Appointment


## Appointment

Stores:

- Doctor
- Patient
- Appointment DateTime
- Status
- Cancellation Reason



# Business Rules

The API enforces the following rules:

- Appointments cannot be booked in the past.
- Appointments must be booked at least one hour in advance.
- Appointments must fall within the doctor's working hours.
- A doctor cannot have two appointments at the same time.
- Cancelled appointments cannot be rescheduled.
- Availability excludes booked appointments.

---

# Concurrency Handling

A potential race condition exists when two users attempt to book the same doctor and time simultaneously.

To prevent double booking:

- A database-level **Unique Constraint** is applied on:

```
doctor_id
slot_time
```

Only one appointment can exist for a doctor at a particular time.

If two requests arrive simultaneously:

1. The first transaction succeeds.
2. The database rejects the second transaction.
3. The application catches the resulting `IntegrityError`.
4. A user-friendly error message is returned.

This approach guarantees data integrity even under concurrent requests.

---

# Design Decisions

Several architectural decisions were made during implementation.

### FastAPI

Chosen because it provides:

- High performance
- Automatic OpenAPI documentation
- Excellent type validation

### SQLAlchemy

Chosen because it:

- Simplifies ORM operations
- Supports multiple databases
- Integrates well with Alembic

### PostgreSQL

Chosen because:

- Excellent transactional support
- Strong concurrency guarantees
- Native support on Render

### Service Layer

Business logic was separated from API routes to improve:

- Maintainability
- Testability
- Readability

---

# Trade-offs

Several trade-offs were considered.

### Simplicity vs Scalability

The project uses a monolithic architecture to keep the assessment simple while maintaining good separation of concerns.

### Database Constraint vs Application Locking

Instead of implementing distributed locks or row locking, the project relies on PostgreSQL unique constraints.

This approach is:

- Simpler
- Reliable
- Appropriate for this assessment

---

# API Endpoints

## Appointments

Method	Endpoint	Description
POST	appointments	 Book appointment
PATCH	appointments/{id}/cancel	 Cancel appointment
PATCH	appointments/{id}/reschedule	Reschedule appointment






Method	Endpoint
GET	/doctors/{id}/availability 

## Patients
Method	Endpoint
GET	 /patients/{id}/appointments


# Installation

Clone repository
<https://github.com/collins-coder/Clinic-Booking-API.git >

Create virtual environment
python -m venv venv

Activate
On Windows
venv\Scripts\activate

Install packages
pip install -r requirements.txt

# Environment Variables

Create a `.env` file.
env
DATABASE_URL=your_postgresql_database_url

SECRET_KEY=your_secret_key

ALGORITHM=HS256

# Database Migration

alembic upgrade head

# Seed Database
python -m app.seed

# Run Application
uvicorn app.main:app --reload


# Testing
Run tests
pytest -v

Coverage
pytest --cov=app --cov-report=term-missing











# CI/CD

The project uses **GitHub Actions** for Continuous Integration.

The pipeline:

- Installs dependencies
- Runs automated tests
- Validates every push and pull request

Deployment is handled automatically by **Render** whenever changes are pushed to the deployment branch.

# Assumptions

- Appointment duration is 30 minutes.
- Doctors work fixed daily schedules.
- Only active appointments affect availability.
- Patients can have multiple appointments.
- All appointment times are handled consistently by the application.

---

# Future Improvements

Potential enhancements include:
- JWT Authentication
- Role-based Access Control
- Email Notifications
- SMS Appointment Reminders
- Docker Support
- Calendar Integration
- Doctor Leave Management
- Pagination
- Search and Filtering

---

# Author

Developed as part of a Backend Engineering Technical Assessment using FastAPI, PostgreSQL, SQLAlchemy, Alembic, and Pytest.
