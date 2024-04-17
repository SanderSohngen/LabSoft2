from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Patient(BaseModel):
    id: int
    name: str


class PatientDetail(Patient):
    age: int
    weight: float
    height: int
    gender: str
    dietaryRestrictions: Optional[str] = None
    medical_observation: Optional[str] = None
    nutritionist_observation: Optional[str] = None
    personal_trainer_observation: Optional[str] = None
    psychologist_observation: Optional[str] = None


class Observation(BaseModel):
    observation: str


class Appointment(BaseModel):
    name: str
    datetime: datetime


class Document(BaseModel):
    key: str
