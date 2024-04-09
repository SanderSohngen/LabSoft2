import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_BASE_URL;
const USERS = process.env.REACT_APP_USERS_URL;
const TOKEN = process.env.REACT_APP_TOKEN_URL;
const ME = process.env.REACT_APP_ME_URL;

const usersURL = BASE_URL + USERS;
const tokenURL = BASE_URL + TOKEN;
const userMeURL = usersURL + ME


export const signup = async (userData) => {
  try {
    const response = await axios.post(usersURL, userData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to sign up.');
    } 
    if (error.request) {
      throw new Error('No response from server.');
    } 
    throw new Error('Error', error.message);
  }
};

export const login = async (credentials) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    const response = await axios.post(tokenURL, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to log in.');
    } 
    if (error.request) {
      throw new Error('No response from server.');
    } 
    throw new Error('Error', error.message);
  }
};

export const getUserDetails = async (token) => {
  try {
    const response = await axios.get(userMeURL, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Failed to get user details.');
    } 
    if (error.request) {
      throw new Error('No response from server.');
    } 
    throw new Error('Error', error.message);
  }
};