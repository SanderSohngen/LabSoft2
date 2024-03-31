import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
// import Agendas from './pages/Agendas';
// import Avaliacao from './pages/Avaliacao';
// import PlanoAlimentar from './pages/PlanoAlimentar';
// import Consulta from './pages/Consulta';
import ErrorPage from './pages/ErrorPage';

const routes = createRoutesFromElements(
    <Route element={<MainLayout />}>
      <Route path="/" element={<Home />} />
      {/* <Route path="agendas" element={<Agendas />} />
      <Route path="avaliacao" element={<Avaliacao />} />
      <Route path="plano-alimentar" element={<PlanoAlimentar />} />
      <Route path="consulta" element={<Consulta />} /> */}
      <Route path="*" element={<ErrorPage />} />
    </Route>
);

export const router = createBrowserRouter(routes);
