import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import Schedule from './pages/Schedule';
import Evaluation from './pages/Evaluation';
// import PlanoAlimentar from './pages/PlanoAlimentar';
// import Consulta from './pages/Consulta';
import ErrorPage from './pages/ErrorPage';

const routes = createRoutesFromElements(
    <Route element={<MainLayout />}>
      <Route path="/" element={<Home />} />
      <Route path="agenda" element={<Schedule />} />
      <Route path="avaliacao" element={<Evaluation />} />
      {/* <Route path="plano-alimentar" element={<PlanoAlimentar />} /> */}
      {/* <Route path="consulta" element={<Consulta />} /> */}
      <Route path="*" element={<ErrorPage />} />
    </Route>
);

export const router = createBrowserRouter(routes);
