import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Flex, VStack, Text } from "@chakra-ui/react";
import PatientCard from "../components/PatientCard/PatientCard";
import ExtraInfoAccordion from "../components/ExtraInfoAccordion/ExtraInfoAccordion";
import InputEvaluation from "../components/InputEvaluation/InputEvaluation";
import { useFetchPatientDetails } from '../hooks/usePatientDetails';
import Loading from '../components/Loading/Loading';

function PatientEvaluation() {
    const { patientId } = useParams();
    const { data: patient, isLoading } = useFetchPatientDetails(patientId);

    const [patientInfo, setPatientInfo] = useState(null);
    const [patientNotes, setPatientNotes] = useState([]);

    useEffect(() => {
        if (patient) {
            const {
                medical_observation,
                nutritionist_observation,
                personal_trainer_observation,
                psychologist_observation,
                ...info
            } = patient;
            const notes = [
                {
                    "professional": "Nutricionista",
                    "evaluation": nutritionist_observation
                },
                {
                    "professional": "Médico",
                    "evaluation": medical_observation
                },
                {
                    "professional": "Personal Trainer",
                    "evaluation": personal_trainer_observation
                },
                {
                    "professional": "Psicólogo",
                    "evaluation": psychologist_observation
                },
            ]
            setPatientInfo(info);
            setPatientNotes(notes);
        }
    }, [patient]);

    if (isLoading) return <Loading />;

    return (
        <Flex align="center" alignItems="center" justifyContent="center" p={5} >
            <VStack spacing={4} mb={4} mt={4}>
                <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Avaliação de Paciente</Text>
                <VStack spacing={8}>
                    <PatientCard {...patientInfo} />
                    <ExtraInfoAccordion info={patientNotes} />
                    <InputEvaluation patientId={patientId} />
                </VStack>
            </VStack>
        </Flex>
    );
}

export default PatientEvaluation;