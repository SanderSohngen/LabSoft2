import { useParams } from "react-router-dom";
import { Box, VStack, Text } from "@chakra-ui/react";
import Chat from "../components/Chat/Chat";


function PatientAppointment() {
    const { name } = useParams();
    return (
        <Box flex="1" p={5}>
        <Text fontSize="4xl" mb={4}>Consulta com Paciente </Text>
            <VStack spacing={8} flex="1">
                <Chat user={name} />
            </VStack>
        </Box>
    );
}

export default PatientAppointment;