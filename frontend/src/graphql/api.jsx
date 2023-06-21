import axios from 'axios';

export const getAllUsers = async () => {
  const query = `
    query {
      users {
        email
      }
    }
  `;

  try {
    const response = await axios.post('http://localhost:8000/graphql/', {
      query,
    });
    return response.data.data.users;
  } catch (error) {
    console.error(error);
    throw new Error('Error retrieving users');
  }
};

