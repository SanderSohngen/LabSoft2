import NameSearch from "../components/NameSearch/NameSearch";
import { Box, Text } from '@chakra-ui/react';

function DietPlan() {
    return (
      <Box flex="1" p={5}>
        <Text fontSize="4xl" mb={4}>Plano Alimentar do Paciente</Text>
        <NameSearch basePath='plano-alimentar'/>
      </Box>
    );
}

export default DietPlan;