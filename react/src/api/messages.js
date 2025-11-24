import instance from './axios';

/**
 * Get messages from chat
 * @param {string} token - Bearer token for authorization
 * @param {number} limit - Number of messages to retrieve (1-100, default 50)
 * @param {number} offset - Offset for pagination (default 0)
 * @returns {Promise} Response with messages array and total count
 */
export const getMessages = async (token, limit = 50, offset = 0) => {
  const response = await instance.get('/api/messages', {
    headers: {
      Authorization: `Bearer ${token}`
    },
    params: {
      limit,
      offset
    }
  });
  return response.data;
};

/**
 * Send a message to chat
 * @param {string} token - Bearer token for authorization
 * @param {string} text - Message text (1-1000 characters)
 * @returns {Promise} Response with created message
 */
export const sendMessage = async (token, text) => {
  const response = await instance.post('/api/messages', 
    {
      text
    },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
  return response.data;
};
