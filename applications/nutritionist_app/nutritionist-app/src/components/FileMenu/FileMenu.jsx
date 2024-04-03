import { Box, Button, IconButton, Menu, MenuButton, MenuItem, MenuList, Link } from '@chakra-ui/react';
import { ChevronDownIcon } from '@chakra-ui/icons';



function FileMenu({ fileList }) {
  return (
    <Box >
      <Menu>
        <MenuButton as={Button} aria-label="Options" rightIcon={<ChevronDownIcon />} variant="outline" colorScheme="teal">
            Planos Alimentares Anteriores
        </MenuButton>
        <MenuList>
          {fileList.map(file => (
            <MenuItem key={file.id} as={Link} href={file.url} isExternal download>
              {file.name}
            </MenuItem>
          ))}
        </MenuList>
      </Menu>
    </Box>
  );
}

export default FileMenu;
