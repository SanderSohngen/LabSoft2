import NameSearch from "../components/NameSearch/NameSearch";
import { Box, Text } from '@chakra-ui/react';

function Evaluation() {
    return (
      <Box flex="1" p={5}>
        <Text fontSize="4xl" mb={4}>Avaliação de Paciente</Text>
        <NameSearch />
      </Box>
    );
}

export default Evaluation;