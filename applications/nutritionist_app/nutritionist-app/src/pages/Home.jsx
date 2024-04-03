import { Flex, Text, VStack } from '@chakra-ui/react';
import AvailabilityForm from '../components/AvailabilityForm/AvailabilityForm';

function Home() {
    return (
      <Flex align="center" alignItems="center" justifyContent="center">
      <VStack spacing={4}>
        <Text fontSize="4xl" mb={4}>Atualizar Disponibilidade</Text>
        <AvailabilityForm />
      </VStack>
      </Flex>
    );
  }

export default Home;
