/**
 * Custom hook for managing assignment data.
 * Provides CRUD operations with loading and error states.
 */
import { useState, useEffect, useCallback } from 'react';
import { assignmentApi, getErrorMessage } from '../services/api';
import type { Assignment, AssignmentRequest } from '../types';

/**
 * Hook for managing assignments
 */
export const useAssignments = (filterDate?: string) => {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Fetch all assignments from the API
   */
  const fetchAssignments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await assignmentApi.getAll(filterDate);
      setAssignments(data);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [filterDate]);

  /**
   * Create a new assignment
   */
  const createAssignment = async (assignment: AssignmentRequest): Promise<Assignment | null> => {
    setError(null);
    try {
      const newAssignment = await assignmentApi.create(assignment);
      setAssignments((prev) => [...prev, newAssignment]);
      return newAssignment;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  };

  /**
   * Update an existing assignment
   */
  const updateAssignment = async (
    id: number,
    assignment: AssignmentRequest
  ): Promise<Assignment | null> => {
    setError(null);
    try {
      const updatedAssignment = await assignmentApi.update(id, assignment);
      setAssignments((prev) =>
        prev.map((a) => (a.id === id ? updatedAssignment : a))
      );
      return updatedAssignment;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  };

  /**
   * Delete an assignment
   */
  const deleteAssignment = async (id: number): Promise<boolean> => {
    setError(null);
    try {
      await assignmentApi.delete(id);
      setAssignments((prev) => prev.filter((a) => a.id !== id));
      return true;
    } catch (err) {
      setError(getErrorMessage(err));
      return false;
    }
  };

  // Fetch assignments on mount and when filter changes
  useEffect(() => {
    fetchAssignments();
  }, [fetchAssignments]);

  return {
    assignments,
    loading,
    error,
    refetch: fetchAssignments,
    createAssignment,
    updateAssignment,
    deleteAssignment,
  };
};
