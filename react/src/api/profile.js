import instance from './axios';

/**
 * Get current user profile
 * @param {string} token - Bearer token for authorization
 * @returns {Promise} Response with user profile data
 */
export const getProfile = async (token) => {
  const response = await instance.get('/api/profile', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
