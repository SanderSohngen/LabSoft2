import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const PROFESSIONAL = process.env.REACT_APP_PROFESSIONAL_URL;

const professional_url = BASE_URL + PROFESSIONAL;
const appointments = "appointments";

export const fetchAppointments = async (profession, professionalId, token) => {
  const url = `${professional_url}${profession}/${professionalId}/${appointments}`;
  try {
    const response = await axios.get(url, {
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
