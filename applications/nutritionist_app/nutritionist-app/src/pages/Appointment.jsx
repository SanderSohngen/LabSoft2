import NameSearch from "../components/NameSearch/NameSearch";
import { Box, Text } from '@chakra-ui/react';

function Appointment() {
    return (
      <Box flex="1" p={5}>
        <Text fontSize="4xl" mb={4}>Consulta com Paciente</Text>
        <NameSearch basePath='consulta'/>
      </Box>
    );
}

export default Appointment;