import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import Schedule from './pages/Schedule';
import Evaluation from './pages/Evaluation';
import PatientEvaluation from './pages/PatientEvaluation';
import DietPlan from './pages/DietPlan';
import PatientDietPlan from './pages/PatientDietPlan';
import ErrorPage from './pages/ErrorPage';

const routes = createRoutesFromElements(
    <Route element={<MainLayout />}>
      <Route path="/" element={<Home />} />
      <Route path="agenda" element={<Schedule />} />
      <Route path="avaliacao" element={<Evaluation />} />
      <Route path="avaliacao/:name" element={<PatientEvaluation />} />
      <Route path="plano-alimentar" element={<DietPlan />} />
      <Route path="plano-alimentar/:name" element={<PatientDietPlan />} />
      <Route path="*" element={<ErrorPage />} />
    </Route>
);

export const router = createBrowserRouter(routes);
