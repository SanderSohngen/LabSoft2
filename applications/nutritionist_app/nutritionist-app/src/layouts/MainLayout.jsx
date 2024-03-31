import { Flex } from '@chakra-ui/react';
import Header from '../components/Header/Header';
import Footer from '../components/Footer/Footer';
import { Outlet } from 'react-router-dom';
import { useNavigation } from 'react-router-dom';
import Loading from '../components/Loading/Loading';

function MainLayout() {
    const navigation = useNavigation();

    return (
        <Flex flexDirection="column" minHeight="100vh">
            <Header />
            <Flex flex="1" direction="column" overflowY="auto" justifyContent="center">
            {navigation.state === 'loading' ? <Loading /> : <Outlet />}
        </Flex>
            <Footer />
        </Flex>
    );
}

export default MainLayout;
