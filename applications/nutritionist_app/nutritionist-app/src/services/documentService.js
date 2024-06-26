import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const PATIENT = process.env.REACT_APP_PATIENT_URL;

const patientURL = BASE_URL + PATIENT;
const documents = "documents";

const documentsURL = (patientId) => `${patientURL}${patientId}/${documents}`;

export const fetchDocuments = async (patientId, token) => {
  try {
    const response = await axios.get(documentsURL(patientId), {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch documents.');
    }
    throw new Error('Server did not respond.');
  }
  };
  
  export const postDocument = async (patientId, documentData, token) => {
  try {
    const response = await axios.post(documentsURL(patientId), documentData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
    throw new Error(error.response.data.detail || 'Failed to post document.');
    }
    throw new Error('Server did not respond.');
  }
  };

const documentURL = (patientId, filename) => `${patientURL}${patientId}/document/${filename}`;

export const downloadDocument = async (patientId, filename, token) => {
  try {
    const response = await axios.get(documentURL(patientId, filename), {
    headers: { 'Authorization': `Bearer ${token}` },
    responseType: 'blob',
    });
    return response.data;
  } catch (error) {
    if (error.response) {
    throw new Error(error.response.data.detail || 'Failed to download document.');
    }
    throw new Error('Server did not respond.');
  }
};