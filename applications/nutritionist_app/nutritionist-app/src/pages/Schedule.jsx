import Calendar from '../components/Calendar/Calendar';
import { Flex, Text, VStack } from '@chakra-ui/react';

function Schedule() {
  return (
    <Flex align="center" alignItems="center" justifyContent="center" p={5} >
        <VStack spacing={4} mb={4} mt={4}>
            <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Agenda</Text>
            <Calendar />
        </VStack>
    </Flex>
  );
}

export default Schedule;
