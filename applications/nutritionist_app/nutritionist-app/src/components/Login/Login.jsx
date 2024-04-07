import React from 'react';
import { Box, Input, Button, useToast } from '@chakra-ui/react';

const Login = () => {
    const toast = useToast();

    const handleSubmit = (e) => {
      e.preventDefault();

        toast({
            title: 'Login successful',
            status:'success',
            duration: 3000,
            isClosable: true,
        });
    };


  return (
    <Box width="md">
      <form onSubmit={handleSubmit}>
        <Input placeholder="E-mail" mb={4} type="email" isRequired={true} />
        <Input placeholder="Senha" mb={4} type="password" isRequired={true} />
        <Button width="full" mt={4} type="submit" colorScheme='teal'>
          Entrar
        </Button>
      </form>
    </Box>
  );
};

export default Login;
