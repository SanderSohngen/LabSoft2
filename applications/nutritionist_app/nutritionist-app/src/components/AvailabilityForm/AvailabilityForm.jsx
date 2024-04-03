import { useState } from 'react';
import {
    Box,
    Button,
    Checkbox,
    CheckboxGroup,
    FormControl,
    FormLabel,
    RangeSlider,
    RangeSliderFilledTrack,
    RangeSliderThumb,
    RangeSliderTrack,
    Text,
    useToast,
    Stack,
} from '@chakra-ui/react';

const daysTranslator = {
    "Monday": "Segunda",
    "Tuesday": "Terça",
    "Wednesday": "Quarta",
    "Thursday": "Quinta",
    "Friday": "Sexta",
  };

function AvailabilityForm() {
    const [days, setDays] = useState([]);
    const [hourRange, setHourRange] = useState([8, 18]);
    const toast = useToast();

    const handleDayChange = (selectedDays) => setDays(selectedDays);
    const translatedDays = days.map(day => daysTranslator[day]);


    const handleSubmit = () => {
        toast({
        title: "Disponibilidade atualizada",
        description: `Sua disponibilidade de ${translatedDays.join(', ')} foi atualizada para as ${hourRange[0]}:00 às ${hourRange[1]}:00.`,
        status: "success",
        duration: 3000,
        isClosable: true,
        });
    };

    return (
        <Box p={5} maxWidth="600px" borderWidth="1px" borderRadius="lg" overflow="hidden">
        <FormControl>
            <FormLabel>Dias da Semana</FormLabel>
            <CheckboxGroup colorScheme="blue" onChange={handleDayChange}>
            <Stack spacing={[1, 5]} direction={['column', 'row']}>
              {Object.entries(daysTranslator).map(([englishDay, portugueseDay]) => (
                <Checkbox key={englishDay} value={englishDay}>{portugueseDay}</Checkbox>
              ))}
            </Stack>
            </CheckboxGroup>
        </FormControl>

        <FormControl mt={6}>
          <FormLabel>Horários Disponíveis</FormLabel>
          <RangeSlider aria-label={['start-time', 'end-time']} defaultValue={[8, 18]} min={8} max={18} onChangeEnd={val => setHourRange(val)}>
            <RangeSliderTrack>
              <RangeSliderFilledTrack />
            </RangeSliderTrack>
            <RangeSliderThumb index={0} />
            <RangeSliderThumb index={1} />
          </RangeSlider>
          <Text textAlign="center" mt={2}>{`${hourRange[0]}:00 - ${hourRange[1]}:00`}</Text>
        </FormControl>

        <Button mt={4} colorScheme="teal" onClick={handleSubmit} isDisabled={days.length === 0}>
            Atualizar
        </Button>
        </Box>
    );
}

export default AvailabilityForm;
