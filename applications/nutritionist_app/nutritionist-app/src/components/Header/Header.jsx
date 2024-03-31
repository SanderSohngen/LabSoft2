import { useNavigate, useLocation } from 'react-router-dom';
import { Flex, Tabs, TabList, Tab, Text } from '@chakra-ui/react';


import { Link } from 'react-router-dom';

function Header() {
    const navigate = useNavigate();
    const location = useLocation();
    const currentPath = location.pathname;

    const handleTabsChange = (index) => {
        const paths = ['/', '/agendas', '/avaliacao', '/plano-alimentar', '/consulta'];
        navigate(paths[index]);
    };

    const tabIndexes = {
        '/': 0,
        '/agendas': 1,
        '/avaliacao': 2,
        '/plano-alimentar': 3,
        '/consulta': 4,
    };
    const currentTabIndex = tabIndexes[currentPath] || 0;

    return (
        <Flex as="header" bg="customPalette.900" color="white" align="center" justify="space-between" padding="4" boxShadow="sm">
        <Text fontSize="xl" fontWeight="bold">VitaLink - Nutricionista</Text>
        <Tabs index={currentTabIndex} onChange={handleTabsChange}>
            <TabList>
            <Tab as={Link} to="/">Home</Tab>
            <Tab as={Link} to="/agendas">Agenda</Tab>
            <Tab as={Link} to="/avaliacao">Avaliação</Tab>
            <Tab as={Link} to="/plano-alimentar">Plano Alimentar</Tab>
            <Tab as={Link} to="/consulta">Consulta</Tab>
            </TabList>
        </Tabs>
        </Flex>
    );
}

export default Header;
