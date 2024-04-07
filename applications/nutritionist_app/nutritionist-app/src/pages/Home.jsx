import { Flex, Text, VStack, Button } from '@chakra-ui/react';
import AvailabilityForm from '../components/AvailabilityForm/AvailabilityForm';
import AuthTabs from '../components/AuthTabs/AuthTabs';
import { useAuth } from '../context/AuthContext';

function Home() {
    const { isLoggedIn, login, logout } = useAuth();
    return (
        <Flex align="center" alignItems="center" justifyContent="center">
        <VStack spacing={4}>
            {
                isLoggedIn? (
                    <>
                    <Text fontSize="4xl" mb={4}>Atualizar Disponibilidade</Text>
                    <AvailabilityForm />
                    <Button colorScheme="red" onClick={logout}>Logout</Button>
                    </>
                ) : (
                    <>
                        <AuthTabs />
                        <Button colorScheme="teal" onClick={() => login({})}>Login</Button> {/* Button to simulate login */}
                    </>
                )
            }
        </VStack>
        </Flex>
    );
};

export default Home;
