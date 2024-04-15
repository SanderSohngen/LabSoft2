from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Patient(BaseModel):
    id: int
    name: str


class PatientDetail(Patient):
    age: int
    weight: float
    height: int
    gender: str
    dietaryRestrictions: Optional[str] = None
    notes: List[dict]


class Appointment(BaseModel):
    name: str
    datetime: datetime


class DocumentUpload(BaseModel):
    documentId: str
    url: Optional[HttpUrl] = None


class Document(DocumentUpload):
    profession: str
    uploaded: datetime


class Observation(BaseModel):
    observation: str
