import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const AVAILABILITY = process.env.REACT_APP_TIMESLOT_URL;
const ME = process.env.REACT_APP_ME_URL;

const availabilityURL = BASE_URL + AVAILABILITY;
const myAvailabilityURL = availabilityURL + ME;

export const submitAvailability = async (availabilityData, token) => {
  try {
    const response = await axios.post(availabilityURL, availabilityData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to submit availability.');
    }
    if (error.request) {
      throw new Error('No response from server.');
    }
    throw new Error('Error', error.message);
  }
};

export const fetchAvailability = async (token) => {
  try {
    const response = await axios.get(myAvailabilityURL, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch availability.');
    }
    if (error.request) {
      throw new Error('No response from server.');
    }
    throw new Error('Error', error.message);
  }
};