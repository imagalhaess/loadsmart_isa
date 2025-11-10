/**
 * Truck Management Component
 * Handles CRUD operations for trucks with form and table view.
 */
import { useState } from 'react';
import { useTrucks } from '../hooks/useTrucks';
import { LicenseType, type Truck, type TruckRequest } from '../types';

export const TruckManagement = () => {
  const { trucks, loading, error, createTruck, updateTruck, deleteTruck } = useTrucks();
  const [formData, setFormData] = useState<TruckRequest>({
    plate: '',
    minimum_license_type: LicenseType.A,
  });
  const [editingId, setEditingId] = useState<number | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  /**
   * Handle form submission for create/update
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMessage(null);

    if (editingId) {
      const result = await updateTruck(editingId, formData);
      if (result) {
        setSuccessMessage('Truck updated successfully!');
        resetForm();
      }
    } else {
      const result = await createTruck(formData);
      if (result) {
        setSuccessMessage('Truck created successfully!');
        resetForm();
      }
    }

    // Clear success message after 3 seconds
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  /**
   * Set up form for editing a truck
   */
  const handleEdit = (truck: Truck) => {
    setFormData({
      plate: truck.plate,
      minimum_license_type: truck.minimum_license_type,
    });
    setEditingId(truck.id);
    setSuccessMessage(null);
  };

  /**
   * Handle truck deletion
   */
  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this truck?')) {
      const result = await deleteTruck(id);
      if (result) {
        setSuccessMessage('Truck deleted successfully!');
        setTimeout(() => setSuccessMessage(null), 3000);
      }
    }
  };

  /**
   * Reset form to initial state
   */
  const resetForm = () => {
    setFormData({ plate: '', minimum_license_type: LicenseType.A });
    setEditingId(null);
  };

  return (
    <div>
      <div className="card">
        <h2>{editingId ? 'Edit Truck' : 'Add New Truck'}</h2>

        {error && <div className="error-message">{error}</div>}
        {successMessage && <div className="success-message">{successMessage}</div>}

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="truck-plate">License Plate</label>
            <input
              id="truck-plate"
              type="text"
              value={formData.plate}
              onChange={(e) => setFormData({ ...formData, plate: e.target.value })}
              required
              placeholder="Enter truck plate (e.g., ABC-1234)"
            />
          </div>

          <div className="form-group">
            <label htmlFor="truck-license">Minimum License Type Required</label>
            <select
              id="truck-license"
              value={formData.minimum_license_type}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  minimum_license_type: e.target.value as LicenseType,
                })
              }
              required
            >
              {Object.values(LicenseType).map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              {editingId ? 'Update Truck' : 'Create Truck'}
            </button>
            {editingId && (
              <button type="button" className="btn btn-secondary" onClick={resetForm}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>

      <div className="card">
        <h2>Trucks List</h2>

        {loading ? (
          <div className="loading">Loading trucks...</div>
        ) : trucks.length === 0 ? (
          <div className="empty-state">No trucks found. Create one above!</div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>License Plate</th>
                  <th>Minimum License Required</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {trucks.map((truck) => (
                  <tr key={truck.id}>
                    <td>{truck.id}</td>
                    <td>{truck.plate}</td>
                    <td>{truck.minimum_license_type}</td>
                    <td>
                      <div className="table-actions">
                        <button
                          className="btn btn-primary btn-small"
                          onClick={() => handleEdit(truck)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-danger btn-small"
                          onClick={() => handleDelete(truck.id)}
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
