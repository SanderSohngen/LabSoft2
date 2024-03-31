import Calendar from '../components/Calendar/Calendar';
import { Box, Text } from '@chakra-ui/react';

function Schedule() {
  return (
    <Box flex="1" p={5}>
      <Text fontSize="4xl" mb={4}>Agenda</Text>
      <Calendar />
    </Box>
  );
}

export default Schedule;
