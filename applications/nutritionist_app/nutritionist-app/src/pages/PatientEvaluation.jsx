import { Flex, VStack, Text } from "@chakra-ui/react";
import PatientCard from "../components/PatientCard/PatientCard";
import ExtraInfoAccordion from "../components/ExtraInfoAccordion/ExtraInfoAccordion";
import InputEvaluation from "../components/InputEvaluation/InputEvaluation";

const patientData = {
    name: "Alice",
    sex: "Feminino",
    age: 25,
    weight: 60,
    height: 175,
    dietaryRestrictions: "Alcool, Gluten, Gordura e Cafeína"
}

const evaluationData = [
    {
        professional: "Nutricionista",
        evaluation: "Avaliação nutricional: Alice está com o peso ideal, porém, precisa aumentar a ingestão de proteínas."
    },
    {
        professional: "Personal Trainer",
        evaluation: "Avaliação física: Alice está com um percentual de gordura acima do recomendado, é necessário a prática de atividades físicas."
    }
]

function PatientEvaluation() {
    return (
        <Flex align="center" alignItems="center" justifyContent="center" p={5} >
            <VStack spacing={4} mb={4} mt={4}>
                <Text fontSize="4xl" mb={4} fontWeight="bold" color='gray'>Avaliação de Paciente</Text>
                <VStack spacing={8}>
                    <PatientCard {...patientData} />
                    <ExtraInfoAccordion info={evaluationData} />
                    <InputEvaluation />
                </VStack>
            </VStack>
        </Flex>
    );
}

export default PatientEvaluation;