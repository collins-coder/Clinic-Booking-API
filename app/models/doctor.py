from sqlalchemy import Column, Integer, String, Time, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    work_start = Column(Time, nullable=False)
    work_end = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Doctor(id={self.id}, full_name='{self.full_name}')>"