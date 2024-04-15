import { Box, Button, Menu, MenuButton, MenuItem, MenuList, Link } from '@chakra-ui/react';
import { ChevronDownIcon } from '@chakra-ui/icons';



function FileMenu({ fileList }) {
  console.log(fileList);
  return (
    <Box >
      <Menu>
        <MenuButton as={Button} aria-label="Options" rightIcon={<ChevronDownIcon />} variant="outline" colorScheme="teal">
            Planos Alimentares Anteriores
        </MenuButton>
        <MenuList>
          {fileList.map(file => (
            <MenuItem key={file.documentId} as={Link} href={file.url} isExternal download>
              {file.documentId}.pdf
            </MenuItem>
          ))}
        </MenuList>
      </Menu>
    </Box>
  );
}

export default FileMenu;
