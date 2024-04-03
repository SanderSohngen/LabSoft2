import {
    Box,
    Heading,
    Text,
    Card,
    CardHeader,
    CardBody,
    Stack,
    StackDivider
} from '@chakra-ui/react'

function PatientCard({ name, sex, age, weight, height, dietaryRestrictions, }) {
    return (
        <Card>
        <CardHeader>
            {name}
        </CardHeader>
        <CardBody>
            <Stack divider={<StackDivider />} spacing='4'>
            <Box>
                <Heading size='xs' textTransform='uppercase'>
                Idade e Sexo
                </Heading>
                <Text pt='2' fontSize='sm'>
                {age} anos - {sex}
                </Text>
            </Box>
            <Box>
                <Heading size='xs' textTransform='uppercase'>
                Altura e Peso
                </Heading>
                <Text pt='2' fontSize='sm'>
                {height} cm {weight} kg
                </Text>
            </Box>
            <Box>
                <Heading size='xs' textTransform='uppercase'>
                Restrições Alimentares
                </Heading>
                <Text pt='2' fontSize='sm'>
                {dietaryRestrictions} 
                </Text>
            </Box>
            </Stack>
        </CardBody>
        </Card>
    );
}

export default PatientCard;