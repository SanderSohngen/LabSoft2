import { useParams } from "react-router-dom";
import { Box, VStack, Text } from "@chakra-ui/react";
import PatientCard from "../components/PatientCard/PatientCard";
import ExtraInfoAccordion from "../components/ExtraInfoAccordion/ExtraInfoAccordion";
import InputEvaluation from "../components/InputEvaluation/InputEvaluation";

const patientData = {
    name: "Alice",
    sex: "Feminino",
    age: 25,
    weight: 60,
    height: 175,
    dietaryRestrictions: "Alcohol, Gluten, Fat, Caffeine"
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
    const { name } = useParams();
    return (
        <Box flex="1" p={5}>
        <Text fontSize="4xl" mb={4}>Avaliação de Paciente</Text>
            <VStack spacing={8}>
                <PatientCard {...patientData} />
                <ExtraInfoAccordion info={evaluationData} />
                <InputEvaluation />
            </VStack>
        </Box>
    );
}

export default PatientEvaluation;