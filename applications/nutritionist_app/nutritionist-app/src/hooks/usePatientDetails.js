import { useQuery } from '@tanstack/react-query';
import * as patientDetailsService from '../services/patientDetailsService';
import { useAuth } from '../context/AuthContext';

export const useFetchPatientDetails = (patientId) => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchPatientDetails', patientId],
    queryFn: () => patientDetailsService.fetchPatientDetails(patientId, user.access_token)
  });
};
