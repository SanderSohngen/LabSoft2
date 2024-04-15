import { useQuery, useMutation } from '@tanstack/react-query';
import * as documentService from '../services/documentService';
import { useAuth } from '../context/AuthContext';

export const useFetchDocuments = (patientId, profession) => {
  const { user } = useAuth();
  return useQuery({
    queryKey: ['fetchDocuments', patientId, profession, user.id],
    queryFn: () => documentService.fetchDocuments(patientId, profession, user.id, user.access_token)
  });
};

export const usePostDocument = (patientId, profession) => {
  const { user } = useAuth();
  return useMutation({
    mutationFn: (documentData) => documentService.postDocument(patientId, profession, user.id, documentData, user.access_token)
  });
};
