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
            const { notes, ...info } = patient;
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
                    <InputEvaluation />
                </VStack>
            </VStack>
        </Flex>
    );
}

export default PatientEvaluation;