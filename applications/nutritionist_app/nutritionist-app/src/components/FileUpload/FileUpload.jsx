import { useState } from 'react';
import { Input, FormControl, FormLabel, Box, IconButton, useToast } from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';

function FileUpload() {
    const [file, setFile] = useState(null);
    const [ inputKey, setInputKey ] = useState(Date.now());
    const toast = useToast();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        toast({
            title: 'Arquivo enviado com sucesso',
            description: `O arquivo "${file.name}" foi enviado com sucesso.`,
            status:'success',
            duration: 3000,
            isClosable: true,
        })
        setFile(null);
        setInputKey(Date.now());
    };

    return (
        <Box as="form" onSubmit={handleSubmit}>
            <FormControl display="flex" alignItems="center" gap="4">
                <FormLabel mb="0">Enviar novo Plano Alimentar</FormLabel>
                <Input
                    key={inputKey}
                    type="file"
                    accept='.pdf'
                    placeholder="Selecione o arquivo"
                    onChange={handleFileChange}
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
                    isDisabled={file === null}
                />
            </FormControl>
        </Box>
    );
}

export default FileUpload;