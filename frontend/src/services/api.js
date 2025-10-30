const API_BASE_URL = 'http://localhost:8000/api';

export const generateQuestion = async () => {
  const response = await fetch(`${API_BASE_URL}/generate/strategy`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Failed to generate question');
  }

  return response.json();
};

export const getQuestion = async (id) => {
  const response = await fetch(`${API_BASE_URL}/questions/${id}`);

  if (!response.ok) {
    throw new Error('Failed to fetch question');
  }

  return response.json();
};