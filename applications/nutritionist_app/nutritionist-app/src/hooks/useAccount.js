import { useMutation } from '@tanstack/react-query';
import * as accountService from '../services/accountService';
import { useAuth } from '../context/AuthContext';

export const useSignup = () => {
  return useMutation({
    mutationFn: accountService.signup,
  });
};
  
export const useLogin = () => {
  const { login } = useAuth();

  return useMutation({
    mutationFn: accountService.login,
    onSuccess: async (data) => {
      const userDetails = await accountService.getUserDetails(data.access_token);
		  login({...userDetails, access_token: data.access_token});
    },
  });
};
