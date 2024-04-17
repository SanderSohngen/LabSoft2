import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, List, ListItem } from '@chakra-ui/react';
import { useFetchPatients } from '../../hooks/usePatient';
import Loading from '../Loading/Loading';


function NameSearch({ basePath }) {
  const [inputValue, setInputValue] = useState('');
  const { data: patients, isLoading } = useFetchPatients();
  const [filteredNames, setFilteredNames] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const sortedList = patients?.sort((a, b) => a.name.localeCompare(b.name));
    const filtered = sortedList?.filter(patient =>
      patient.name.toLowerCase().includes(inputValue.toLowerCase())
    );
    setFilteredNames(filtered);
  }, [inputValue, patients]);

  const handleSelectName = (id) => {
    navigate(`/${basePath}/${id}`);
  };

  if (isLoading) return <Loading />;

  return (
    <>
      <Input
        placeholder="Digite um nome"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        name="input"
      />
      {inputValue && (
        <List>
          {filteredNames.length > 0 ? (
            filteredNames.map((patient) => (
              <ListItem key={patient.id} cursor="pointer" onClick={() => handleSelectName(patient.id)}>
                {patient.name}
              </ListItem>
            ))
          ) : (
            <ListItem>Nenhum nome encontrado.</ListItem>
          )}
        </List>
      )}
    </>
  );
}

export default NameSearch;
