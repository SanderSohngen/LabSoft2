import { Flex, Text, VStack } from '@chakra-ui/react';
import FileMenu from '../components/FileMenu/FileMenu';
import FileUpload from '../components/FileUpload/FileUpload';

const mockFiles = [
    { id: 1, name: "DietPlan1.pdf", url: "https://example.com/dietplan1.pdf" },
    { id: 2, name: "DietPlan2.pdf", url: "https://example.com/dietplan2.pdf" },
  ];

function PatientDietPlan() {
    return (
        <Flex align="center" alignItems="center" justifyContent="center" p={5} >
            <VStack spacing={4} mb={4} mt={4}>
                <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Plano Alimentar do Paciente</Text>
                <VStack spacing={8}>
                    <FileUpload />
                    <FileMenu fileList={mockFiles}/>
                </VStack>
            </VStack>
        </Flex>
    );
}

export default PatientDietPlan;