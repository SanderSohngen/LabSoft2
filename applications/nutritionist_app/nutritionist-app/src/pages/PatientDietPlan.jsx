import { useParams } from "react-router-dom";
import { Box, VStack, Text } from "@chakra-ui/react";
import FileMenu from '../components/FileMenu/FileMenu';
import FileUpload from '../components/FileUpload/FileUpload';

const mockFiles = [
    { id: 1, name: "DietPlan1.pdf", url: "https://example.com/dietplan1.pdf" },
    { id: 2, name: "DietPlan2.pdf", url: "https://example.com/dietplan2.pdf" },
  ];

function PatientDietPlan() {
    const { name } = useParams();
    return (
        <Box flex="1" p={5}>
        <Text fontSize="4xl" mb={4}>Plano Alimentar do Paciente</Text>
            <VStack spacing={8}>
                <FileUpload />
                <FileMenu fileList={mockFiles}/>
            </VStack>
        </Box>
    );
}

export default PatientDietPlan;