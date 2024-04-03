import { useRef } from 'react';
import { Input, FormControl, FormLabel, Box, IconButton } from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';

function InputEvaluation() {
    const textFieldRef = useRef(null);

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(textFieldRef.current.value);
        textFieldRef.current.value = '';
    };

    return (
        <Box as="form" onSubmit={handleSubmit}>
            <FormControl display="flex" alignItems="center" gap="4">
                <FormLabel mb="0">Atualizar avaliação:</FormLabel>
                <Input
                    ref={textFieldRef}
                    placeholder="Digite aqui a avaliação"
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
                />
            </FormControl>
        </Box>
    );
}

export default InputEvaluation;
