import { useRef, useState } from 'react';
import { Input, FormControl, FormLabel, Box, IconButton, useToast } from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';

function InputEvaluation() {
    const textFieldRef = useRef(null);
    const [isInputEmpty, setIsInputEmpty] = useState(true);
    const toast = useToast();

    const handleInputChange = (e) => {
        setIsInputEmpty(e.target.value.trim() === '');
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        toast({
            title: 'Avaliação enviada com sucesso',
            description: 'Avaliação atualizada para "' + textFieldRef.current.value + '"',
            status:'success',
            duration: 3000,
            isClosable: true,
        })
        textFieldRef.current.value = '';
        setIsInputEmpty(true);
    };

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
                    spinner="true"
                    icon={<CheckIcon />}
                    isDisabled={isInputEmpty}
                />
            </FormControl>
        </Box>
    );
}

export default InputEvaluation;
