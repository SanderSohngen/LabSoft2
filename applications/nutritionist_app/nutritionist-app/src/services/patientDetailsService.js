import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const PATIENT = process.env.REACT_APP_PATIENT_URL;

const patient_url = BASE_URL + PATIENT;
const details = "details";

export const fetchPatientDetails = async (patientId, token) => {
  const url = `${patient_url}${patientId}/${details}`;
  try {
    const response = await axios.get(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch patient details.');
    }
    throw new Error('Server did not respond.');
  }
};
