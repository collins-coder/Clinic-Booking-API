from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("postgresql://clinic_booking_m1gd_user:fkB92UHenVYChRJupyktdMFyC6CV3aGc@dpg-d98v2n3tqb8s739qrt90-a.oregon-postgres.render.com/clinic_booking_m1gd")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file.")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()