/**
 * Assignment Management Component
 * Handles CRUD operations for driver-truck assignments with validation.
 */
import { useState } from 'react';
import { useAssignments } from '../hooks/useAssignments';
import { useDrivers } from '../hooks/useDrivers';
import { useTrucks } from '../hooks/useTrucks';
import type { Assignment, AssignmentRequest } from '../types';

export const AssignmentManagement = () => {
  const [filterDate, setFilterDate] = useState<string>('');
  const { assignments, loading, error, createAssignment, updateAssignment, deleteAssignment } =
    useAssignments(filterDate || undefined);
  const { drivers } = useDrivers();
  const { trucks } = useTrucks();

  const [formData, setFormData] = useState<AssignmentRequest>({
    driver_id: 0,
    truck_id: 0,
    assignment_date: new Date().toISOString().split('T')[0], // Today's date
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  /**
   * Get driver name by ID
   */
  const getDriverName = (driverId: number): string => {
    const driver = drivers.find((d) => d.id === driverId);
    return driver ? `${driver.name} (${driver.license_type})` : `Driver #${driverId}`;
  };

  /**
   * Get truck plate by ID
   */
  const getTruckPlate = (truckId: number): string => {
    const truck = trucks.find((t) => t.id === truckId);
    return truck ? `${truck.plate} (Requires ${truck.minimum_license_type})` : `Truck #${truckId}`;
  };

  /**
   * Handle form submission for create/update
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMessage(null);

    // Validate that driver and truck are selected
    if (formData.driver_id === 0 || formData.truck_id === 0) {
      return;
    }

    if (editingId) {
      const result = await updateAssignment(editingId, formData);
      if (result) {
        setSuccessMessage('Assignment updated successfully!');
        resetForm();
      }
    } else {
      const result = await createAssignment(formData);
      if (result) {
        setSuccessMessage('Assignment created successfully!');
        resetForm();
      }
    }

    // Clear success message after 3 seconds
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  /**
   * Set up form for editing an assignment
   */
  const handleEdit = (assignment: Assignment) => {
    setFormData({
      driver_id: assignment.driver_id,
      truck_id: assignment.truck_id,
      assignment_date: assignment.assignment_date,
    });
    setEditingId(assignment.id);
    setSuccessMessage(null);
  };

  /**
   * Handle assignment deletion
   */
  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this assignment?')) {
      const result = await deleteAssignment(id);
      if (result) {
        setSuccessMessage('Assignment deleted successfully!');
        setTimeout(() => setSuccessMessage(null), 3000);
      }
    }
  };

  /**
   * Reset form to initial state
   */
  const resetForm = () => {
    setFormData({
      driver_id: 0,
      truck_id: 0,
      assignment_date: new Date().toISOString().split('T')[0],
    });
    setEditingId(null);
  };

  return (
    <div>
      <div className="card">
        <h2>{editingId ? 'Edit Assignment' : 'Create New Assignment'}</h2>

        {error && <div className="error-message">{error}</div>}
        {successMessage && <div className="success-message">{successMessage}</div>}

        {drivers.length === 0 || trucks.length === 0 ? (
          <div className="error-message">
            You must have at least one driver and one truck to create assignments.
            {drivers.length === 0 && <div>Please create a driver first.</div>}
            {trucks.length === 0 && <div>Please create a truck first.</div>}
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="form">
            <div className="form-group">
              <label htmlFor="assignment-driver">Driver</label>
              <select
                id="assignment-driver"
                value={formData.driver_id}
                onChange={(e) =>
                  setFormData({ ...formData, driver_id: Number(e.target.value) })
                }
                required
              >
                <option value={0}>Select a driver...</option>
                {drivers.map((driver) => (
                  <option key={driver.id} value={driver.id}>
                    {driver.name} - License: {driver.license_type}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="assignment-truck">Truck</label>
              <select
                id="assignment-truck"
                value={formData.truck_id}
                onChange={(e) =>
                  setFormData({ ...formData, truck_id: Number(e.target.value) })
                }
                required
              >
                <option value={0}>Select a truck...</option>
                {trucks.map((truck) => (
                  <option key={truck.id} value={truck.id}>
                    {truck.plate} - Requires: {truck.minimum_license_type}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="assignment-date">Assignment Date</label>
              <input
                id="assignment-date"
                type="date"
                value={formData.assignment_date}
                onChange={(e) =>
                  setFormData({ ...formData, assignment_date: e.target.value })
                }
                required
              />
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={formData.driver_id === 0 || formData.truck_id === 0}
              >
                {editingId ? 'Update Assignment' : 'Create Assignment'}
              </button>
              {editingId && (
                <button type="button" className="btn btn-secondary" onClick={resetForm}>
                  Cancel
                </button>
              )}
            </div>
          </form>
        )}
      </div>

      <div className="card">
        <h2>Assignments List</h2>

        <div className="form-group" style={{ marginBottom: '20px' }}>
          <label htmlFor="filter-date">Filter by Date (optional)</label>
          <input
            id="filter-date"
            type="date"
            value={filterDate}
            onChange={(e) => setFilterDate(e.target.value)}
            placeholder="Filter by date..."
          />
          {filterDate && (
            <button
              type="button"
              className="btn btn-secondary btn-small"
              onClick={() => setFilterDate('')}
              style={{ marginTop: '8px' }}
            >
              Clear Filter
            </button>
          )}
        </div>

        {loading ? (
          <div className="loading">Loading assignments...</div>
        ) : assignments.length === 0 ? (
          <div className="empty-state">
            {filterDate
              ? `No assignments found for ${filterDate}`
              : 'No assignments found. Create one above!'}
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Driver</th>
                  <th>Truck</th>
                  <th>Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {assignments.map((assignment) => (
                  <tr key={assignment.id}>
                    <td>{assignment.id}</td>
                    <td>{getDriverName(assignment.driver_id)}</td>
                    <td>{getTruckPlate(assignment.truck_id)}</td>
                    <td>{assignment.assignment_date}</td>
                    <td>
                      <div className="table-actions">
                        <button
                          className="btn btn-primary btn-small"
                          onClick={() => handleEdit(assignment)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-danger btn-small"
                          onClick={() => handleDelete(assignment.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
