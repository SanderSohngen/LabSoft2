import { useNavigate, useLocation } from 'react-router-dom';
import { Flex, Tabs, TabList, Tab, Text } from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function Header() {
    const navigate = useNavigate();
    const location = useLocation();
    const currentPath = location.pathname;
    const { isLoggedIn } = useAuth();

    const paths = ['/', '/agenda', '/avaliacao', '/plano-alimentar', '/consulta'];

    const currentTabIndex = paths.findLastIndex(path => currentPath.startsWith(path));

    const handleTabsChange = (index) => {
        navigate(paths[index]);
    };

    return (
        <Flex as="header" bg="customPalette.900" color="white" align="center" justify="space-between" padding="4" boxShadow="sm">
        <Text fontSize="xl" fontWeight="bold">VitaLink - Nutricionista</Text>
        <Tabs index={currentTabIndex} onChange={handleTabsChange}>
            <TabList>
            <Tab as={Link} to="/">Home</Tab>
            {isLoggedIn && (
                <>
                    <Tab as={Link} to="/agenda">Agenda</Tab>
                    <Tab as={Link} to="/avaliacao">Avaliação</Tab>
                    <Tab as={Link} to="/plano-alimentar">Plano Alimentar</Tab>
                    <Tab as={Link} to="/consulta">Consulta</Tab>
                </>
            )}
            </TabList>
        </Tabs>
        </Flex>
    );
}

export default Header;
