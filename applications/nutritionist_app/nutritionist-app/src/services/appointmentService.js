import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const PROFESSIONAL = process.env.REACT_APP_PROFESSIONAL_URL;

const professionalURL = BASE_URL + PROFESSIONAL;
const appointments = "appointments";

const appointmentsURL = professionalURL + appointments

export const fetchAppointments = async (token) => {
  try {
    const response = await axios.get(appointmentsURL, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch appointments.');
    }
    throw new Error('Server did not respond.');
  }
};
