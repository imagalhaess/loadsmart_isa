/**
 * Custom hook for managing truck data.
 * Provides CRUD operations with loading and error states.
 */
import { useState, useEffect, useCallback } from 'react';
import { truckApi, getErrorMessage } from '../services/api';
import type { Truck, TruckRequest } from '../types';

/**
 * Hook for managing trucks
 */
export const useTrucks = () => {
  const [trucks, setTrucks] = useState<Truck[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch all trucks from the API
   */
  const fetchTrucks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await truckApi.getAll();
      setTrucks(data);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Create a new truck
   */
  const createTruck = async (truck: TruckRequest): Promise<Truck | null> => {
    setError(null);
    try {
      const newTruck = await truckApi.create(truck);
      setTrucks((prev) => [...prev, newTruck]);
      return newTruck;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  };

  /**
   * Update an existing truck
   */
  const updateTruck = async (id: number, truck: TruckRequest): Promise<Truck | null> => {
    setError(null);
    try {
      const updatedTruck = await truckApi.update(id, truck);
      setTrucks((prev) =>
        prev.map((t) => (t.id === id ? updatedTruck : t))
      );
      return updatedTruck;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  };

  /**
   * Delete a truck
   */
  const deleteTruck = async (id: number): Promise<boolean> => {
    setError(null);
    try {
      await truckApi.delete(id);
      setTrucks((prev) => prev.filter((t) => t.id !== id));
      return true;
    } catch (err) {
      setError(getErrorMessage(err));
      return false;
    }
  };

  // Fetch trucks on mount
  useEffect(() => {
    fetchTrucks();
  }, [fetchTrucks]);

  return {
    trucks,
    loading,
    error,
    refetch: fetchTrucks,
    createTruck,
    updateTruck,
    deleteTruck,
  };
};
