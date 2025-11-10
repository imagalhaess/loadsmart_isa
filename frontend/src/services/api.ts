/**
 * API service for communicating with the backend.
 * Centralizes all HTTP requests using axios.
 */
import axios, { AxiosError } from 'axios';
import type {
  Driver,
  DriverRequest,
  Truck,
  TruckRequest,
  Assignment,
  AssignmentRequest,
  ApiError,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Extracts error message from API error response
 */
export const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    return axiosError.response?.data?.detail || 'An unexpected error occurred';
  }
  return 'An unexpected error occurred';
};

/**
 * Driver API endpoints
 */
export const driverApi = {
  /**
   * Get all drivers
   */
  getAll: async (): Promise<Driver[]> => {
    const response = await api.get<Driver[]>('/drivers');
    return response.data;
  },

  /**
   * Get a driver by ID
   */
  getById: async (id: number): Promise<Driver> => {
    const response = await api.get<Driver>(`/drivers/${id}`);
    return response.data;
  },

  /**
   * Create a new driver
   */
  create: async (driver: DriverRequest): Promise<Driver> => {
    const response = await api.post<Driver>('/drivers', driver);
    return response.data;
  },

  /**
   * Update a driver
   */
  update: async (id: number, driver: DriverRequest): Promise<Driver> => {
    const response = await api.put<Driver>(`/drivers/${id}`, driver);
    return response.data;
  },

  /**
   * Delete a driver
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/drivers/${id}`);
  },
};

/**
 * Truck API endpoints
 */
export const truckApi = {
  /**
   * Get all trucks
   */
  getAll: async (): Promise<Truck[]> => {
    const response = await api.get<Truck[]>('/trucks');
    return response.data;
  },

  /**
   * Get a truck by ID
   */
  getById: async (id: number): Promise<Truck> => {
    const response = await api.get<Truck>(`/trucks/${id}`);
    return response.data;
  },

  /**
   * Create a new truck
   */
  create: async (truck: TruckRequest): Promise<Truck> => {
    const response = await api.post<Truck>('/trucks', truck);
    return response.data;
  },

  /**
   * Update a truck
   */
  update: async (id: number, truck: TruckRequest): Promise<Truck> => {
    const response = await api.put<Truck>(`/trucks/${id}`, truck);
    return response.data;
  },

  /**
   * Delete a truck
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/trucks/${id}`);
  },
};

/**
 * Assignment API endpoints
 */
export const assignmentApi = {
  /**
   * Get all assignments, optionally filtered by date
   */
  getAll: async (date?: string): Promise<Assignment[]> => {
    const params = date ? { assignment_date: date } : undefined;
    const response = await api.get<Assignment[]>('/assignments', { params });
    return response.data;
  },

  /**
   * Get an assignment by ID
   */
  getById: async (id: number): Promise<Assignment> => {
    const response = await api.get<Assignment>(`/assignments/${id}`);
    return response.data;
  },

  /**
   * Create a new assignment
   */
  create: async (assignment: AssignmentRequest): Promise<Assignment> => {
    const response = await api.post<Assignment>('/assignments', assignment);
    return response.data;
  },

  /**
   * Update an assignment
   */
  update: async (id: number, assignment: AssignmentRequest): Promise<Assignment> => {
    const response = await api.put<Assignment>(`/assignments/${id}`, assignment);
    return response.data;
  },

  /**
   * Delete an assignment
   */
  delete: async (id: number): Promise<void> => {
    await api.delete(`/assignments/${id}`);
  },
};
