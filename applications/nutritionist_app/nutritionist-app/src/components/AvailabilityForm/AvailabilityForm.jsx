import { Grid, Box, Button, useToast } from '@chakra-ui/react';
import { useState, useEffect } from 'react';
import { useSubmitAvailability, useFetchAvailability } from '../../hooks/useAvailability';
import Loading from '../Loading/Loading';

const daysOfWeek = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];
const timeSlots = Array.from({ length: 10 }, (_, i) => `${(8 + i).toString().padStart(2, '0')}:00`);


function AvailabilityForm() {
	const [availability, setAvailability] = useState({});
	const { data: myTimeSlots, isLoading } = useFetchAvailability();
	const submitAvailability = useSubmitAvailability();
	const toast = useToast();

	useEffect(() => {
        if (myTimeSlots) {
            const newAvailability = myTimeSlots.reduce((acc, slot) => {
                const [hours, minutes] = slot.time.split(":").slice(0, 2);
                const formattedTime = `${hours}:${minutes}`;
                const day = daysOfWeek[slot.day_of_week];
                acc[day] = acc[day] || [];
                acc[day].push(formattedTime);
                return acc;
              }, {});
              setAvailability(newAvailability);
        }
    }, [myTimeSlots]);

    if (isLoading) {
        return <Loading />;
    }
    
	
	const toggleSlot = (day, time) => {
        const dayAvailability = availability[day] || [];
        if (dayAvailability.includes(time)) {
            setAvailability({
                ...availability,
                [day]: dayAvailability.filter(t => t !== time),
            });
        } else {
            setAvailability({
                ...availability,
                [day]: [...dayAvailability, time],
            });
        }
	};

	const handleSubmit = () => {
        const availabilityData = daysOfWeek.flatMap((day, index) => 
			(availability[day] || []).map(time => ({
				day_of_week: index,
				time
			}))
		);
		submitAvailability.mutateAsync(availabilityData, {
			onSuccess: () => {
				toast({
					title: 'Disponibilidade atualizada',
					description: 'Sua disponibilidade foi atualizada com sucesso.',
					status: 'success',
					duration: 3000,
					isClosable: true,
				});
			},
            onError: (error) => {
                toast({
                    title: 'Submissão falhou',
                    description: error.message || 'Ocorreu um erro ao tentar atualizar.',
                    status: 'error',
                    duration: 3000,
                    isClosable: true,
                });
            }
        });
	};
	
	return (
		<Box p={6} borderWidth="1px" borderRadius="lg" overflow="hidden">
		<Grid templateColumns={`repeat(${daysOfWeek.length}, 1fr)`} gap={4}>
			{daysOfWeek.map(day => (
			<Box key={day} textAlign="center" fontWeight="semibold" color='gray'>
				{day}
			</Box>
			))}
			{timeSlots.map(time => (
			daysOfWeek.map(day => (
				<Button
                    key={`${day}-${time}`}
                    colorScheme={availability[day]?.includes(time) ? 'teal' : 'gray'}
                    onClick={() => toggleSlot(day, time)}
                    size="sm"
                    _hover={{ bg: 'teal.100' }}
				>
				{time}
				</Button>
			))
			))}
		</Grid>
		<Button
			mt={6}
			colorScheme="teal"
			width="full"
			onClick={handleSubmit}
		>
			Atualizar
		</Button>
		</Box>
	);
}

export default AvailabilityForm;
