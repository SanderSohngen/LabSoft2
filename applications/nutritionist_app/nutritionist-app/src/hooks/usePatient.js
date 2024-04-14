import { useQuery } from '@tanstack/react-query';
import * as patientService from '../services/patientService';
import { useAuth } from '../context/AuthContext';

export const useFetchPatients = (profession) => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchPatients', profession, user.id],
    queryFn: () => patientService.fetchPatients(profession, user.id, user.access_token),
  });
};
