import { CircularProgress, Center } from '@chakra-ui/react';

function Loading() {
  return (
    <Center h="100vh">
      <CircularProgress isIndeterminate color="customPalette.700" />
    </Center>
  );
}

export default Loading;
