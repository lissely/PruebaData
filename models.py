from datetime import datetime
from sqlalchemy import Column, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import uuid
import enum  # Importamos enum de Python
from sqlalchemy.types import Uuid # Import Uuid type
from database import Base

# Definimos el Enum de Python
class RoleEnum(str, enum.Enum):
    TRAINER = "Trainer"
    NUTRICIONIST = "Nutricionist"
    ADMINISTRATOR = "Administrator"


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4(), index=True)
    name = Column(String(50))
    lastName = Column(String(50))
    phone = Column(String(20))
    email = Column(String(50), unique=True, index=True)
    password = Column(String(72))
    salary = Column(Float)
    date_of_contract = Column(DateTime, default=datetime.utcnow)

    role = Column(String(15), default=RoleEnum.TRAINER, nullable=False)

    sede_id = Column(Uuid, ForeignKey('sede.id'), nullable=False)
    sede = relationship("Sede", back_populates="employees")


class Sede(Base):
    __tablename__ = 'sede'

    id = Column(Uuid, primary_key=True, default=uuid.uuid4(), index=True)
    name = Column(String(50))
    address = Column(String(50))
    phone = Column(String(50))

    employees = relationship("Employees", back_populates="sede", cascade="all, delete-orphan")    