from typing import List
from httpx import AsyncClient
from fastapi import Depends, APIRouter, HTTPException

from ..dependency import get_client
from ..external_schemas import (
    Patient,
    PatientDetail,
    Appointment,
    Document,
    DocumentUpload,
    Observation
)


router = APIRouter()


@router.get(
    "/professional/{profession}/{professional_id}/patients",
    response_model=List[Patient]
)
async def get_patients(
    profession: str,
    professional_id: int,
    client: AsyncClient = Depends(get_client)
) -> List[Patient]:
    response = await client.get(
        f"/professional/{profession}/{professional_id}/patients"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar pacientes"
        )
    return response.json()


@router.get(
    "/professional/{profession}/{professional_id}/appointments",
    response_model=List[Appointment]
)
async def get_appointments(
    profession: str,
    professional_id: int,
    client: AsyncClient = Depends(get_client)
) -> List[Appointment]:
    response = await client.get(
        f"/professional/{profession}/{professional_id}/appointments"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar compromissos"
        )
    return response.json()


@router.get(
    "/patient/{patient_id}/details",
    response_model=PatientDetail
)
async def get_patient_details(
    patient_id: int,
    client: AsyncClient = Depends(get_client)
) -> PatientDetail:
    response = await client.get(
        f"/patient/{patient_id}/details"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar detalhes do paciente"
        )
    return response.json()


@router.get(
    "/patient/{patient_id}/{profession}/{professional_id}/documents",
    response_model=List[Document]
)
async def get_documents(
    patient_id: int,
    profession: str,
    professional_id: int,
    client: AsyncClient = Depends(get_client)
) -> List[Document]:
    response = await client.get(
        f"/patient/{patient_id}/{profession}/{professional_id}/documents"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar documentos"
        )
    return [Document(**doc) for doc in response.json()]


@router.post(
    "/patient/{patient_id}/{profession}/{professional_id}/observation",
    response_model=dict
)
async def post_observation(
    patient_id: int,
    profession: str,
    professional_id: int,
    observation: Observation,
    client: AsyncClient = Depends(get_client)
) -> dict:
    response = await client.post(
        f"/patient/{patient_id}/{profession}/{professional_id}/observation",
        json=observation.model_dump_json()
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao adicionar observação"
        )
    return {"message": "Observação adicionada com sucesso"}


@router.post(
    "/patient/{patient_id}/{profession}/{professional_id}/documents",
    response_model=dict
)
async def post_documents(
    patient_id: int,
    profession: str,
    professional_id: int,
    document_data: DocumentUpload,
    client: AsyncClient = Depends(get_client)
) -> dict:
    response = await client.post(
        f"/patient/{patient_id}/{profession}/{professional_id}/documents",
        json=document_data.model_dump_json()
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao carregar o documento"
        )
    return {"message": "Documento enviado com sucesso"}
