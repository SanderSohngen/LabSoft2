import { useQuery } from '@tanstack/react-query';
import * as appointmentService from '../services/appointmentService';
import { useAuth } from '../context/AuthContext';

export const useFetchAppointments = (profession) => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchAppointments', profession, user.id],
    queryFn: () => appointmentService.fetchAppointments(profession, user.id, user.access_token),
  });
};
