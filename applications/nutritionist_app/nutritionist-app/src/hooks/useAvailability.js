import { useMutation, useQuery } from '@tanstack/react-query';
import * as availabilityService from '../services/availabilityService';
import { useAuth } from '../context/AuthContext';

export const useSubmitAvailability = () => {
  const { user } = useAuth();

  return useMutation({
    mutationFn: (availabilityData) => {
      const payload = availabilityData.map(data => ({
        ...data,
         user_id: user.id,
      }))
      return availabilityService.submitAvailability(payload, user.access_token)
    },
  });
};

export const useFetchAvailability = () => {
  const { user } = useAuth();

  return useQuery({
    queryKey: ['fetchAvailability', user.id],
    queryFn: () => availabilityService.fetchAvailability(user.access_token)
  })
};