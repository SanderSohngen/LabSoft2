import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box
} from '@chakra-ui/react';

function ExtraInfoAccordion({ info }) {
  return (
    <Accordion allowToggle>
      {info.map((item, index) => (
        <AccordionItem key={index}>
          <h2>
            <AccordionButton>
              <Box flex="1" textAlign="left">
                {item.professional}
              </Box>
              <AccordionIcon />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4}>
            {item.evaluation}
          </AccordionPanel>
        </AccordionItem>
      ))}
    </Accordion>
  );
}

export default ExtraInfoAccordion;
