import random

from datetime import datetime, timedelta
from .external_schemas import (
    Patient,
    PatientDetail,
    Appointment,
    Document,
    DocumentUpload,
    Observation
)


def generate_weekday_appointments():
    appointments = []

    base_date = datetime.now()
    while base_date.weekday() >= 5:
        base_date += timedelta(days=1)

    for i in range(30):
        days_to_add = random.randint(-15, 15)
        appointment_date = base_date + timedelta(days=days_to_add)

        while appointment_date.weekday() >= 5:
            appointment_date += timedelta(days=1)

        hour = random.randint(8, 17)
        appointment_time = appointment_date.replace(hour=hour, minute=0, second=0, microsecond=0)

        appointments.append(
            Appointment(
                name=f"Consulta {i + 1}",
                datetime=appointment_time.isoformat()
            )
        )

    return appointments


def generate_mock_patients():
    mock_patients = [
        Patient(id=1, name='Alice'),
        Patient(id=2, name='Bob'),
        Patient(id=3, name='Charlie'),
        Patient(id=4, name='David'),
        Patient(id=5, name='Eve')
    ]
    return mock_patients


def generate_mock_patient_detail(patient_id):
    patients = [
        {'id': 1, 'name': 'Alice', 'gender': 'Feminino'},
        {'id': 2, 'name': 'Bob', 'gender': 'Masculino'},
        {'id': 3, 'name': 'Charlie', 'gender': 'Masculino'},
        {'id': 4, 'name': 'David', 'gender': 'Masculino'},
        {'id': 5, 'name': 'Eve', 'gender': 'Feminino'}
    ]
    dietary_restrictions = [
        "Nenhuma",
        "Vegana",
        "Sem glúten",
        "Sem nozes",
        "Sem lactose",
        "Baixo carboidrato",
        "Cetogênica"
    ]
    professional_evaluations = {
        "Nutricionista": [
            "Necessita de maior ingestão de vitaminas",
            "Deve aumentar a ingestão de proteínas",
            "Recomenda-se dieta com baixa ingestão de sódio"
        ],
        "Psicólogo": [
            "Requer acompanhamento psicológico contínuo",
            "Apresenta sinais de estresse, recomendável terapia",
            "Sugere-se tratamento para ansiedade"
        ],
        "Personal Trainer": [
            "Deve evitar atividades físicas intensas devido a problemas cardíacos",
            "Está em excelente condição física, continuar com o regime atual",
            "Necessita iniciar atividades físicas regulares para melhorar a condição física"
        ],
        "Médico": [
            "Tem histórico familiar de diabetes, requer atenção",
            "Recomenda-se vacinação anual contra gripe",
            "Deve continuar o tratamento para hipertensão"
        ]
    }
    patient = next(p for p in patients if p['id'] == patient_id)
    notes = []
    for professional, evals in professional_evaluations.items():
        notes.append({
            "professional": professional,
            "evaluation": random.choice(evals)
        })

    return PatientDetail(
        id=patient['id'],
        name=patient['name'],
        age=random.randint(18, 60),
        weight=round(random.uniform(50.0, 120.0), 1),
        height=int(random.uniform(150.0, 200.0)),
        gender=patient['gender'],
        dietaryRestrictions=random.choice(dietary_restrictions),
        notes=random.sample(notes, k=random.randint(1, len(notes)))
    )


def generate_mock_documents():
    documents = []

    num_of_documents = random.randint(1, 5)
    for i in range(num_of_documents):
        documents.append(
            Document(
                documentId=f"doc_{i + 1}",
                url=f"https://example.com/doc_{i + 1}",
                profession="nutricionista",
                uploaded=datetime.now() - timedelta(days=random.randint(0, 365))
            )
        )
    return documents
