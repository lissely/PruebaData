import datetime
from fastapi import FastAPI, HTTPException, Depends, status # type: ignore
from pydantic import BaseModel, EmailStr # type: ignore
from typing import Annotated, List, Optional
from passlib.context import CryptContext

from sqlalchemy import create_engine, text # type: ignore
import models
from database import Base, SessionLocal, engine # type: ignore
from sqlalchemy.orm import Session # type: ignore
import uuid

models.Base.metadata.create_all(bind=engine)

# Crea una instancia de la aplicación FastAPI
app = FastAPI()


# Define un modelo Pydantic para la validación de datos
class EmployeeBase(BaseModel):
    id: uuid.UUID | None = None
    name: str
    lastName: str
    password: str
    phone: str
    email: str
    salary: float | None = None
    date_of_contract: datetime.datetime | None = None
    sede_id: uuid.UUID | None = None

class Sede(BaseModel):
    name: str
    address: str | None = None
    phone: str

#Dtos
class LoginCredentialsRequest(BaseModel):
    email: EmailStr
    password: str # Contraseña en texto plano para validar
    userType: str | None = None # Tipo de usuario (opcional)

class UserValidationResponse(BaseModel): # Respuesta para AuthService
    userId: uuid.UUID
    email: EmailStr
    hashedPassword: str
    roles: List[str]


# Crea una base de datos de ejemplo
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Para injecion de dependencias:
db_dependency = Annotated[Session, Depends(get_db)]

#Endopoints par empleados
@app.post("/employees", response_model=EmployeeBase, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeBase, db: db_dependency):
    db_employee = models.Employees(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/{employee_id}", response_model=EmployeeBase)
async def read_employee(employee_id: uuid.UUID, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

#Endpoints para autenticacion
@app.post("/employees/credentials", response_model=UserValidationResponse)
async def login_employee(employee: LoginCredentialsRequest, db: db_dependency):
    db_employee = db.query(models.Employees).filter(models.Employees.email == employee.email).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return UserValidationResponse(
        userId=db_employee.id,
        email=db_employee.email,
        hashedPassword=db_employee.password,
        roles= ["ROLE_EMPLOYEE"]
    )

#Endpoints para sedes
@app.post("/sede", response_model=Sede, status_code=status.HTTP_201_CREATED)
async def create_sede(sede: Sede, db: db_dependency):
    db_sede = models.Sede(**sede.dict())
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede

@app.get("/sede/{sede_id}", response_model=Sede)
async def read_sede(sede_id: uuid.UUID, db: db_dependency):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede not found")
    return db_sede

@app.get("/sede", response_model=list[Sede])
async def read_all_sedes(db: db_dependency):
    db_sedes = db.query(models.Sede).all()
    return db_sedes