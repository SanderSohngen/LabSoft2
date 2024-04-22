import NameSearch from "../components/NameSearch/NameSearch";
import { Flex, Text, VStack } from '@chakra-ui/react';

function Evaluation() {
    return (
      <Flex align="center" alignItems="center" justifyContent="center" p={5} >
          <VStack spacing={4} mb={4} mt={4}>
              <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Avaliação de Paciente</Text>
              <NameSearch basePath='avaliacao'/>
          </VStack>
      </Flex>
    );
}

export default Evaluation;