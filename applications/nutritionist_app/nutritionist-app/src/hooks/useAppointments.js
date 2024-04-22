import { useQuery } from '@tanstack/react-query';
import * as appointmentService from '../services/appointmentService';
import { useAuth } from '../context/AuthContext';

export const useFetchAppointments = () => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchAppointments', user.id],
    queryFn: () => appointmentService.fetchAppointments(user.access_token),
  });
};
