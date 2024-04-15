import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const PATIENT = process.env.REACT_APP_PATIENT_URL;

const patient_url = BASE_URL + PATIENT;
const documents = "documents";

export const fetchDocuments = async (patientId, profession, professionalId, token) => {
	const url = `${patient_url}${patientId}/${profession}/${professionalId}/${documents}`;
	try {
	  const response = await axios.get(url, {
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
  
  export const postDocument = async (patientId, profession, professionalId, documentData, token) => {
	const url = `${patient_url}${patientId}/${profession}/${professionalId}/${documents}`;
	try {
	  const response = await axios.post(url, documentData, {
		headers: {
		  'Authorization': `Bearer ${token}`,
		  'Content-Type': 'application/json'
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