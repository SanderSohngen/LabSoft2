import os
import boto3

from typing import List
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from httpx import AsyncClient
from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from botocore.exceptions import ClientError

from ..dependency import get_current_user
from ..external_dependency import get_client, get_s3_client
from ..models import User
from ..external_schemas import (
    Patient,
    PatientDetail,
    Observation,
    Appointment,
    Document,
)
from ..external_s3_file_manager import (
    upload_doc_to_s3,
    download_doc_from_s3,
)


router = APIRouter()

load_dotenv()
EXTERNAL_API_URL = os.getenv("EXTERNAL_BASE_URL")
PROFESSION = "nutritionist"
PROFESSIONAL_ID = 3
PATIENT_ID = 1


@router.get(
    "/professional/patients",
    response_model=List[Patient]
)
async def get_patients(
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> List[Patient]:
    response = await client.get(
        f"{EXTERNAL_API_URL}/professionals/{PROFESSION}/{PROFESSIONAL_ID}/patients/"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar pacientes"
        )
    return [
        Patient(**patient)
        for patient in response.json()
    ]


@router.get(
    "/professional/appointments",
    response_model=List[Appointment]
)
async def get_appointments(
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> List[Appointment]:
    response = await client.get(
        f"{EXTERNAL_API_URL}/professionals/{PROFESSION}/{PROFESSIONAL_ID}/appointments/"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar compromissos"
        )
    return [
        Appointment(**appointment)
        for appointment in response.json()
    ]


@router.get(
    "/patient/{patient_id}/details",
    response_model=PatientDetail
)
async def get_patient_details(
    patient_id: int,
    _: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> PatientDetail:
    response = await client.get(
        f"{EXTERNAL_API_URL}/patients/{PATIENT_ID}/details/"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar detalhes do paciente"
        )

    return PatientDetail(**response.json())


@router.post(
    "/patient/{patient_id}/observation",
    response_model=dict
)
async def post_observation(
    patient_id: int,
    observation_data: Observation,
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client)
) -> dict:
    response = await client.post(
        f"{EXTERNAL_API_URL}/patients/{PATIENT_ID}/{PROFESSION}/{PROFESSIONAL_ID}/observation/",
        json={"observation": observation_data.observation}
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao adicionar observação"
        )
    return {"message": "Observação adicionada com sucesso"}


@router.get(
    "/patient/{patient_id}/documents",
    response_model=List[Document]
)
async def get_documents(
    patient_id: int,
    # user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client),
    s3_client: boto3.client = Depends(get_s3_client)
) -> List[Document]:
    response = await client.get(
        f"{EXTERNAL_API_URL}/patients/{PATIENT_ID}/{PROFESSION}/{PROFESSIONAL_ID}/getdocuments/"
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao buscar documentos"
        )
    return [Document(**doc) for doc in response.json()]


@router.get(
    "/patient/{patient_id}/document/{filename:path}",
    response_model=dict
)
def download_document(
    patient_id: int,
    filename: str,
    user: User = Depends(get_current_user),
    s3_client: boto3.client = Depends(get_s3_client)
):
    try:
        return StreamingResponse(
            download_doc_from_s3(patient_id, user.id, filename, s3_client),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except ClientError as e:
        detail = e.response['Error'].get('Message', 'Unknown error')
        raise HTTPException(status_code=404, detail=detail)


@router.post(
    "/patient/{patient_id}/documents",
    response_model=dict
)
async def post_documents(
    patient_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    client: AsyncClient = Depends(get_client),
    s3_client: boto3.client = Depends(get_s3_client)
) -> dict:
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    document_data = upload_doc_to_s3(
        patient_id=patient_id,
        user=user,
        s3_client=s3_client,
        file=file
    )
    response = await client.post(
        f"{EXTERNAL_API_URL}/patients/{PATIENT_ID}/{PROFESSION}/{PROFESSIONAL_ID}/postdocuments/",
        json=document_data.model_dump()
    )
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code,
            detail="Falha ao carregar o documento"
        )
    return {"message": "Documento enviado com sucesso"}
