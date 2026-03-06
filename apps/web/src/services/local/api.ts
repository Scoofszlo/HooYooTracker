import axios from 'axios';

const api = axios.create({
  baseURL: "http://localhost:3000/",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  }
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!navigator.onLine) {
      return Promise.reject(new Error("You are offline. Please check your internet connection."));
    }

    return Promise.reject(error);
  },
);

export default api;
