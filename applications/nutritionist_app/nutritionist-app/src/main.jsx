import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { CharkraProvider } from '@chakra-ui/react'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <CharkraProvider>
      <App />
    </CharkraProvider>
    <App />
  </React.StrictMode>,
)
