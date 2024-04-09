import {
    Box,
    Input,
    Button,
    useToast,
    FormControl,
    FormErrorMessage,
} from '@chakra-ui/react';
import { useState } from 'react';
import { useSignup, useLogin } from '../../hooks/useAccount';
import { validateSignupForm } from '../../validation';
import Loading from '../Loading/Loading';

const Signup = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [formErrors, setFormErrors] = useState({});
    const signup = useSignup();
    const login = useLogin();
    const toast = useToast();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const errors = validateSignupForm(formData);

        if (Object.keys(errors).length > 0) {
            setFormErrors(errors);
            return;
        }
        const { confirmPassword, ...signupData } = formData;

        signup.mutateAsync(signupData, {
            onSuccess: () => {
                login.mutateAsync({ email: signupData.email, password: signupData.password }, {
                    onSuccess: () => {
                        toast({
                            title: 'Conta criada',
                            description: `Olá, ${signupData.name}, sua conta foi criada e você será logado.`,
                            status: 'success',
                            duration: 3000,
                            isClosable: true,
                        });
                    }
                });
            },
            onError: (error) => {
                toast({
                    title: 'Falha ao criar conta.',
                    description: error.message || "Ocorreu um erro ao criar conta.",
                    status: 'error',
                    duration: 3000,
                    isClosable: true,
                });
            }
        });
    };

    return (
        <>
        <Box width="md">
            <form onSubmit={handleSubmit} >
                <FormControl mb={4}>
                    <Input name="name" placeholder="Nome" value={formData.name} onChange={handleInputChange} isRequired />
                </FormControl>
                <FormControl mb={4} isInvalid={!!formErrors.email}>
                    <Input name="email" placeholder="E-mail" value={formData.email} onChange={handleInputChange} isRequired />
                    <FormErrorMessage>{formErrors.email}</FormErrorMessage>
                </FormControl>
                <FormControl mb={4}>
                    <Input name="password" placeholder="Senha" type="password" value={formData.password} onChange={handleInputChange} isRequired />
                </FormControl>
                    <FormControl mb={4} isInvalid={!!formErrors.confirmPassword}>
                    <Input name="confirmPassword" placeholder="Confirmar senha" type="password" value={formData.confirmPassword} onChange={handleInputChange} isRequired />
                    <FormErrorMessage>{formErrors.confirmPassword}</FormErrorMessage>
                </FormControl>
                <Button width="full" mt={4} type="submit" colorScheme='teal' >
                    Inscrever-se
                </Button>
            </form>
        </Box>
        { (signup.isPending || login.isPending) && <Loading />}
        </>
    );
};



export default Signup;
