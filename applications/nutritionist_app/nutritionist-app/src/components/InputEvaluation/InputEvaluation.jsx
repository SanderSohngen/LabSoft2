import { useRef, useState } from 'react';
import { Input, FormControl, FormLabel, Box, IconButton, useToast } from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';
import { usePostObservation } from '../../hooks/usePatientDetails';
import Loading from '../Loading/Loading';

function InputEvaluation({ patientId }) {
    const textFieldRef = useRef(null);
    const [isInputEmpty, setIsInputEmpty] = useState(true);
    const toast = useToast();
    const { mutate: postObservation, isPending } = usePostObservation(patientId);

    const handleInputChange = (e) => {
        setIsInputEmpty(e.target.value.trim() === '');
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const observationData = { "observation": textFieldRef.current.value };
        postObservation(observationData, {
            onSuccess: () => {
                toast({
                    title: 'Avaliação enviada com sucesso',
                    description: 'Avaliação atualizada para "' + textFieldRef.current.value + '"',
                    status:'success',
                    duration: 3000,
                    isClosable: true,
                });
                textFieldRef.current.value = '';
                setIsInputEmpty(true);
            }
        });
    };

    if (isPending) return <Loading />;

    return (
        <Box as="form" onSubmit={handleSubmit}>
            <FormControl display="flex" alignItems="center" gap="4">
                <FormLabel mb="0">Atualizar avaliação:</FormLabel>
                <Input
                    ref={textFieldRef}
                    placeholder="Digite aqui a avaliação"
                    onChange={handleInputChange}
                />
                <IconButton
                    type="submit"
                    isRound={true}
                    variant='solid'
                    colorScheme='teal'
                    aria-label='Done'
                    fontSize='20px'
                    isLoading={isPending}
                    icon={<CheckIcon />}
                    isDisabled={isInputEmpty || isPending}
                />
            </FormControl>
        </Box>
    );
}

export default InputEvaluation;
