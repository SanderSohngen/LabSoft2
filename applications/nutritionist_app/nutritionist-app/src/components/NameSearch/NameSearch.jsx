import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, List, ListItem } from '@chakra-ui/react';

const allNames = ['Alice', 'Bob', 'Charlie', 'David', 'Eve'];

function NameSearch({ basePath }) {
  const [inputValue, setInputValue] = useState('');
  const [filteredNames, setFilteredNames] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (inputValue) {
      const newFilteredNames = allNames.filter(name =>
        name.toLowerCase().includes(inputValue.toLowerCase())
      );
      setFilteredNames(newFilteredNames);
    } else {
      setFilteredNames([]);
    }
  }, [inputValue]);

  const handleSelectName = (name) => {
    navigate(`/${basePath}/${name}`);
  };

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
            filteredNames.map((name, index) => (
              <ListItem key={index} cursor="pointer" onClick={() => handleSelectName(name)}>
                {name}
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
