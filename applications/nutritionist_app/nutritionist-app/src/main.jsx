import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from './routes';
import { ChakraProvider } from '@chakra-ui/react';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
import theme from './theme';
import './main.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <ChakraProvider theme={theme}>
        <RouterProvider router={router} >
          <ProtectedRoute />
        </RouterProvider>
      </ChakraProvider>
    </AuthProvider>
  </React.StrictMode>
);
