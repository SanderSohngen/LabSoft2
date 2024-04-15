from typing import List
from httpx import AsyncClient
from fastapi import Depends, APIRouter, HTTPException

from ..dependency import get_client, get_current_user
from ..models import User
from ..external_schemas import (
    Patient,
    PatientDetail,
    Appointment,
    Document,
    DocumentUpload,
    Observation
)
from ..mock_data_generator import (
    generate_mock_patients,
    generate_weekday_appointments,
    generate_mock_patient_detail,
    generate_mock_documents,
)


router = APIRouter()
PROFESSION = "nutritionist"


@router.get(
    "/professional/patients",
    response_model=List[Patient]
)
async def get_patients(
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> List[Patient]:
    return generate_mock_patients()

    response = await client.get(
        f"/professional/{PROFESSION}/{user.id}/patients"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar pacientes"
        )
    return response.json()


@router.get(
    "/professional/appointments",
    response_model=List[Appointment]
)
async def get_appointments(
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> List[Appointment]:
    return generate_weekday_appointments()

    response = await client.get(
        f"/professional/{PROFESSION}/{user.id}/appointments"
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
    _: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> PatientDetail:
    return generate_mock_patient_detail(patient_id)

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
    "/patient/{patient_id}/documents",
    response_model=List[Document]
)
async def get_documents(
    patient_id: int,
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> List[Document]:
    return generate_mock_documents()

    response = await client.get(
        f"/patient/{patient_id}/{PROFESSION}/{user.id}/documents"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar documentos"
        )
    return [Document(**doc) for doc in response.json()]


@router.post(
    "/patient/{patient_id}/observation",
    response_model=dict
)
async def post_observation(
    patient_id: int,
    observation: Observation,
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> dict:
    response = await client.post(
        f"/patient/{patient_id}/{PROFESSION}/{user.id}/observation",
        json=observation.model_dump_json()
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao adicionar observação"
        )
    return {"message": "Observação adicionada com sucesso"}


@router.post(
    "/patient/{patient_id}/documents",
    response_model=dict
)
async def post_documents(
    patient_id: int,
    document_data: DocumentUpload,
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> dict:
    response = await client.post(
        f"/patient/{patient_id}/{PROFESSION}/{user.id}/documents",
        json=document_data.model_dump_json()
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao carregar o documento"
        )
    return {"message": "Documento enviado com sucesso"}
