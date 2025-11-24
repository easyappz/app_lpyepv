import instance from './axios';

/**
 * Register a new user
 * @param {string} username - Username (3-50 characters)
 * @param {string} password - Password (minimum 6 characters)
 * @returns {Promise} Response with token
 */
export const registerUser = async (username, password) => {
  const response = await instance.post('/api/register', {
    username,
    password
  });
  return response.data;
};

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise} Response with token
 */
export const loginUser = async (username, password) => {
  const response = await instance.post('/api/login', {
    username,
    password
  });
  return response.data;
};
