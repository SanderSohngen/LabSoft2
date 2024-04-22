import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const PATIENT = process.env.REACT_APP_PATIENT_URL;

const patientURL = BASE_URL + PATIENT;
const details = "details";
const observation = "observation";

const detailsURL = (patientId) => `${patientURL}${patientId}/${details}`;

export const fetchPatientDetails = async (patientId, token) => {
  try {
    const response = await axios.get(detailsURL(patientId), {
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


const observationURL = (patientId) => `${patientURL}${patientId}/${observation}`;

export const postPatientObservation = async (patientId, observationData, token) => {
  try {
    const response = await axios.post(observationURL(patientId), observationData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to post patient observation.');
    }
    throw new Error('Server did not respond.');
  }
};