import { useQuery } from '@tanstack/react-query';
import * as patientService from '../services/patientService';
import { useAuth } from '../context/AuthContext';

export const useFetchPatients = () => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchPatients', user.id],
    queryFn: () => patientService.fetchPatients(user.access_token),
  });
};
