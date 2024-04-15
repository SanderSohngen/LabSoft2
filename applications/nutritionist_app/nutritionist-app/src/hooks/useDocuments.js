import { useQuery, useMutation } from '@tanstack/react-query';
import * as documentService from '../services/documentService';
import { useAuth } from '../context/AuthContext';

export const useFetchDocuments = (patientId) => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchDocuments', patientId],
    queryFn: () => documentService.fetchDocuments(patientId, user.access_token)
  });
};

export const usePostDocument = (patientId) => {
  const { user } = useAuth();
  return useMutation({
    mutationFn: (documentData) => documentService.postDocument(patientId, documentData, user.access_token)
  });
};
