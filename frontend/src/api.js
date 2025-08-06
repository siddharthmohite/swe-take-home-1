/**
 * API service module for making requests to the backend
 */

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

/**
 * Fetch climate data with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateData = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams({
      ...(filters.locationId && { location_id: filters.locationId }),
      ...(filters.startDate && { start_date: filters.startDate }),
      ...(filters.endDate && { end_date: filters.endDate }),
      ...(filters.metric && { metric: filters.metric }),
      ...(filters.qualityThreshold && { quality_threshold: filters.qualityThreshold })
    }).toString();
    const response = await fetch(`${API_BASE_URL}/climate?${queryParams}`);
    if (!response.ok) throw new Error('Failed to fetch climate data');
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch all available locations
 * @returns {Promise} - API response
 */
export const getLocations = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/locations`);
    if (!response.ok) throw new Error('Failed to fetch locations');
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch all available metrics
 * @returns {Promise} - API response
 */
export const getMetrics = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/metrics`);
    if (!response.ok) throw new Error('Failed to fetch metrics');
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch climate summary statistics with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateSummary = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams({
      ...(filters.locationId && { location_id: filters.locationId }),
      ...(filters.startDate && { start_date: filters.startDate }),
      ...(filters.endDate && { end_date: filters.endDate }),
      ...(filters.metric && { metric: filters.metric }),
      ...(filters.qualityThreshold && { quality_threshold: filters.qualityThreshold })
    }).toString();
    const response = await fetch(`${API_BASE_URL}/summary?${queryParams}`);
    if (!response.ok) throw new Error('Failed to fetch summary');
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getTrendAnalysis = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams({
      ...(filters.locationId && { location_id: filters.locationId }),
      ...(filters.startDate && { start_date: filters.startDate }),
      ...(filters.endDate && { end_date: filters.endDate }),
      ...(filters.metric && { metric: filters.metric }),
      ...(filters.qualityThreshold && { quality_threshold: filters.qualityThreshold })
    }).toString();
    const response = await fetch(`${API_BASE_URL}/trends?${queryParams}`);
    if (!response.ok) throw new Error('Failed to fetch trends');
    return response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};