import { Box, Menu, MenuButton, Button, MenuList, MenuItem, useToast } from '@chakra-ui/react';
import { ChevronDownIcon } from '@chakra-ui/icons';
import { saveAs } from 'file-saver';
import { useDownloadDocument } from '../../hooks/useDocuments';
import Loading from '../Loading/Loading';
import { useFetchDocuments } from '../../hooks/useDocuments';

function FileMenu({  patientId }) {
    const { data: files } = useFetchDocuments(patientId);
    const { mutate: downloadDocument, isPending } = useDownloadDocument(patientId);
	const toast = useToast();

    const handleDownload = async (filename) => {
        downloadDocument({ patientId, filename },
            {
            onSuccess: (data) => {
                const blob = new Blob([data], { type: 'application/pdf' });
                saveAs(blob, `${filename}`);
                toast({
					title: 'Arquivo baixado',
					description: `O arquivo ${filename} foi baixado com sucesso.`,
					status: 'success',
					duration: 3000,
					isClosable: true,
				});
            },
            onError: (error) => {
                toast({
                    title: 'Download falhou',
                    description: error.message || 'Ocorreu um erro ao tentar atualizar.',
                    status: 'error',
                    duration: 3000,
                    isClosable: true,
                });
            }
            },
        );
    };

  if (isPending) return <Loading />;

  if (!files || files.length === 0) {
    return (
      <Box>
        <Menu>
          <MenuButton as={Button} aria-label="Options" rightIcon={<ChevronDownIcon />} variant="outline" colorScheme="teal">
            Planos Alimentares Anteriores
          </MenuButton>
          <MenuList>
            <MenuItem isDisabled>Nenhum arquivo ainda</MenuItem>
          </MenuList>
        </Menu>
      </Box>
    );
  }

  return (
    <Box>
      <Menu>
        <MenuButton as={Button} aria-label="Options" rightIcon={<ChevronDownIcon />} variant="outline" colorScheme="teal">
          Planos Alimentares Anteriores
        </MenuButton>
        <MenuList>
            {files && files?.map(file => {
                const filename = file.key.split('/').pop()
                return (
                    <MenuItem key={file.key} onClick={() => handleDownload(filename)}>
                        {filename}
                    </MenuItem>
                );
            })}
        </MenuList>
      </Menu>
    </Box>
  );
};

export default FileMenu;