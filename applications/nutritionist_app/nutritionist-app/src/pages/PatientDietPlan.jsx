import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Flex, VStack, Text } from "@chakra-ui/react";
import { useFetchDocuments, usePostDocument } from '../hooks/useDocuments';
import FileMenu from '../components/FileMenu/FileMenu';
import FileUpload from '../components/FileUpload/FileUpload';
import Loading from '../components/Loading/Loading';

function PatientDietPlan() {
    const { patientId } = useParams();
    const profession = "Nutricionista";

    const { data: files, isLoading } = useFetchDocuments(patientId, profession);
    const [fileList, setFileList] = useState([]);
    const { mutate: postDocument } = usePostDocument(patientId, profession);

    useEffect(() => {
        if (files && files.length > 0) {
            setFileList(files);
        }
    }, [files]);

    const handleFileUpload = (fileData) => {
        postDocument(fileData, {
            onSuccess: () => {
            },
            onError: (error) => {
                console.error("Error uploading document:", error);
            }
        });
    };

    if (isLoading) return <Loading />;

    return (
        <Flex align="center" alignItems="center" justifyContent="center" p={5}>
            <VStack spacing={4} mb={4} mt={4}>
                <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Plano Alimentar do Paciente</Text>
                <VStack spacing={8}>
                    <FileUpload onUpload={handleFileUpload} />
                    <FileMenu fileList={fileList} />
                </VStack>
            </VStack>
        </Flex>
    );
}

export default PatientDietPlan;
