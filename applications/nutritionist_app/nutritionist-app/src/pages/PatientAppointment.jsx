import Chat from "../components/Chat/Chat";
import { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import Loading from '../components/Loading/Loading';
import { Box, VStack, Text } from "@chakra-ui/react";
import { useFetchPatients } from '../hooks/usePatient';


function PatientAppointment() {
    const { patientId } = useParams();
    const { data: patients, isLoading } = useFetchPatients("nutritionist");
    const [patientName, setPatientName] = useState("");

    useEffect(() => {
        const id = parseInt(patientId);
        const patient = patients?.find(patient => patient.id === id);
        setPatientName(patient?.name);
    }, [patientId, patients]);

    if (isLoading) return <Loading />;

    return (
        <Box flex="1" p={5}>
            <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Consulta com Paciente</Text>
            <VStack spacing={8} flex="1">
                <Chat user={patientName} />
            </VStack>
        </Box>
    );
}

export default PatientAppointment;