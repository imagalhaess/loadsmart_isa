/**
 * Custom hook for managing driver data.
 * Provides CRUD operations with loading and error states.
 */
import { useState, useEffect, useCallback } from 'react';
import { driverApi, getErrorMessage } from '../services/api';
import type { Driver, DriverRequest } from '../types';

/**
 * Hook for managing drivers
 */
export const useDrivers = () => {
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch all drivers from the API
   */
  const fetchDrivers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await driverApi.getAll();
      setDrivers(data);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Create a new driver
   */
  const createDriver = async (driver: DriverRequest): Promise<Driver | null> => {
    setError(null);
    try {
      const newDriver = await driverApi.create(driver);
      setDrivers((prev) => [...prev, newDriver]);
      return newDriver;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  };

  /**
   * Update an existing driver
   */
  const updateDriver = async (id: number, driver: DriverRequest): Promise<Driver | null> => {
    setError(null);
    try {
      const updatedDriver = await driverApi.update(id, driver);
      setDrivers((prev) =>
        prev.map((d) => (d.id === id ? updatedDriver : d))
      );
      return updatedDriver;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  };

  /**
   * Delete a driver
   */
  const deleteDriver = async (id: number): Promise<boolean> => {
    setError(null);
    try {
      await driverApi.delete(id);
      setDrivers((prev) => prev.filter((d) => d.id !== id));
      return true;
    } catch (err) {
      setError(getErrorMessage(err));
      return false;
    }
  };

  // Fetch drivers on mount
  useEffect(() => {
    fetchDrivers();
  }, [fetchDrivers]);

  return {
    drivers,
    loading,
    error,
    refetch: fetchDrivers,
    createDriver,
    updateDriver,
    deleteDriver,
  };
};
