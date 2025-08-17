import axios from 'axios';

// Base URL for our API calls
// We use a relative URL because we set up a proxy in package.json
const API_BASE_URL = '/api';

// Create an axios instance with some default settings
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,  // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json'
  }
});

// Function to handle API errors in a simple way
export const handleAPIError = (error) => {
  // If the error has a response from the server
  if (error.response) {
    // The server responded with an error status code
    const status = error.response.status;
    const data = error.response.data;
    
    // Return a user-friendly error message
    if (data && data.error) {
      return data.error;
    } else if (status === 404) {
      return 'Resource not found';
    } else if (status === 500) {
      return 'Server error - please try again later';
    } else {
      return `Error ${status}: Something went wrong`;
    }
  } else if (error.request) {
    // The request was made but no response was received
    return 'No response from server - check your internet connection';
  } else {
    // Something else happened while setting up the request
    return 'Error setting up request';
  }
};

// API functions for jobs
export const jobAPI = {
  // Get all jobs with optional filters and pagination
  getJobs: async (params = {}) => {
    try {
      // Make a GET request to /api/jobs with the parameters
      const response = await api.get('/jobs', { params });
      
      // Return the data from the response
      return response.data;
      
    } catch (error) {
      // If something goes wrong, throw the error
      throw error;
    }
  },

  // Get a specific job by ID
  getJob: async (jobId) => {
    try {
      // Make a GET request to /api/jobs/{id}
      const response = await api.get(`/jobs/${jobId}`);
      
      // Return the job data
      return response.data;
      
    } catch (error) {
      throw error;
    }
  },

  // Create a new job
  createJob: async (jobData) => {
    try {
      // Make a POST request to /api/jobs with the job data
      const response = await api.post('/jobs', jobData);
      
      // Return the response data
      return response.data;
      
    } catch (error) {
      throw error;
    }
  },

  // Update an existing job
  updateJob: async (jobId, jobData) => {
    try {
      // Make a PUT request to /api/jobs/{id} with the updated data
      const response = await api.put(`/jobs/${jobId}`, jobData);
      
      // Return the response data
      return response.data;
      
    } catch (error) {
      throw error;
    }
  },

  // Delete a job
  deleteJob: async (jobId) => {
    try {
      // Make a DELETE request to /api/jobs/{id}
      const response = await api.delete(`/jobs/${jobId}`);
      
      // Return the response data
      return response.data;
      
    } catch (error) {
      throw error;
    }
  },

  // Get filter options (job types, locations, tags)
  getFilters: async () => {
    try {
      // Make a GET request to /api/jobs/filters
      const response = await api.get('/jobs/filters');
      
      // Return the filter options
      return response.data;
      
    } catch (error) {
      throw error;
    }
  }
};

// Export the API instance in case we need it elsewhere
export default api;
