import React from 'react';
import { Box, Input, Button, useToast } from '@chakra-ui/react';

const Signup = ( { onSignupSucess } ) => {
    const toast = useToast();

    const handleSubmit = (e) => {
        e.preventDefault();

        toast({
            title: 'Conta criada.',
            description: "Sua conta foi criada com sucesso.",
            status: 'success',
            duration: 9000,
            isClosable: true,
        });

        onSignupSucess();
    };

  return (
    <Box width="md">
        <form onSubmit={handleSubmit} >
        <Input placeholder="Nome" mb={4} type="text" isRequired={true} />
        <Input placeholder="E-mail" mb={4} type="email" isRequired={true} />
        <Input placeholder="Senha" mb={4} type="password" isRequired={true} />
        <Input placeholder="Confirmar Senha" mb={4} type="password" isRequired={true} />
        <Button width="full" mt={4} type="submit" colorScheme='teal'>
            Inscrever-se
        </Button>
        </form>
        
    </Box>
  );
};

export default Signup;
