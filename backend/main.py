from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

DATABASE_URL = "sqlite:///./hospital.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(title="Hospital Management API")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    room_no = Column(String, nullable=False)
    occupation = Column(String, nullable=True)
    guardian_name = Column(String, nullable=True)
    medical_history = Column(Text, nullable=True)
    current_condition = Column(Text, nullable=True)
    surgeries = relationship("Surgery", back_populates="patient")
    medications = relationship("Medication", back_populates="patient")

class Surgery(Base):
    __tablename__ = "surgeries"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="surgeries")

class Medication(Base):
    __tablename__ = "medications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    given_today = Column(Boolean, default=False)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="medications")

Base.metadata.create_all(bind=engine)

class MedicationSchema(BaseModel):
    id: Optional[int]
    name: str
    dosage: str
    given_today: bool
    class Config:
        orm_mode = True

class SurgerySchema(BaseModel):
    id: Optional[int]
    type: str
    date: str
    class Config:
        orm_mode = True

class PatientSchema(BaseModel):
    id: Optional[int]
    name: str
    room_no: str
    occupation: Optional[str]
    guardian_name: Optional[str]
    medical_history: Optional[str]
    current_condition: Optional[str]
    surgeries: List[SurgerySchema] = []
    medications: List[MedicationSchema] = []
    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/patients/", response_model=PatientSchema)
def create_patient(patient: PatientSchema, db: Session = Depends(get_db)):
    db_patient = Patient(
        name=patient.name,
        room_no=patient.room_no,
        occupation=patient.occupation,
        guardian_name=patient.guardian_name,
        medical_history=patient.medical_history,
        current_condition=patient.current_condition
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/patients/", response_model=List[PatientSchema])
def list_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@app.post("/patients/{patient_id}/medications/", response_model=MedicationSchema)
def add_medication(patient_id: int, med: MedicationSchema, db: Session = Depends(get_db)):
    db_med = Medication(name=med.name, dosage=med.dosage, given_today=med.given_today, patient_id=patient_id)
    db.add(db_med)
    db.commit()
    db.refresh(db_med)
    return db_med

@app.post("/patients/{patient_id}/surgeries/", response_model=SurgerySchema)
def add_surgery(patient_id: int, surg: SurgerySchema, db: Session = Depends(get_db)):
    db_surg = Surgery(type=surg.type, date=surg.date, patient_id=patient_id)
    db.add(db_surg)
    db.commit()
    db.refresh(db_surg)
    return db_surg
