import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Flex, VStack, Text } from "@chakra-ui/react";
import { useFetchDocuments, usePostDocument } from '../hooks/useDocuments';
import FileMenu from '../components/FileMenu/FileMenu';
import FileUpload from '../components/FileUpload/FileUpload';
import Loading from '../components/Loading/Loading';

function PatientDietPlan() {
    const { patientId } = useParams();

    return (
        <Flex align="center" alignItems="center" justifyContent="center" p={5}>
            <VStack spacing={4} mb={4} mt={4}>
                <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Plano Alimentar do Paciente</Text>
                <VStack spacing={8}>
                    <FileUpload patientId={patientId}/>
                    <FileMenu patientId={patientId} />
                </VStack>
            </VStack>
        </Flex>
    );
}

export default PatientDietPlan;
