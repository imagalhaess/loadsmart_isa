/**
 * Driver Management Component
 * Handles CRUD operations for drivers with form and table view.
 */
import { useState } from 'react';
import { useDrivers } from '../hooks/useDrivers';
import { LicenseType, type Driver, type DriverRequest } from '../types';

export const DriverManagement = () => {
  const { drivers, loading, error, createDriver, updateDriver, deleteDriver } = useDrivers();
  const [formData, setFormData] = useState<DriverRequest>({
    name: '',
    license_type: LicenseType.A,
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
      const result = await updateDriver(editingId, formData);
      if (result) {
        setSuccessMessage('Driver updated successfully!');
        resetForm();
      }
    } else {
      const result = await createDriver(formData);
      if (result) {
        setSuccessMessage('Driver created successfully!');
        resetForm();
      }
    }

    // Clear success message after 3 seconds
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  /**
   * Set up form for editing a driver
   */
  const handleEdit = (driver: Driver) => {
    setFormData({
      name: driver.name,
      license_type: driver.license_type,
    });
    setEditingId(driver.id);
    setSuccessMessage(null);
  };

  /**
   * Handle driver deletion
   */
  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this driver?')) {
      const result = await deleteDriver(id);
      if (result) {
        setSuccessMessage('Driver deleted successfully!');
        setTimeout(() => setSuccessMessage(null), 3000);
      }
    }
  };

  /**
   * Reset form to initial state
   */
  const resetForm = () => {
    setFormData({ name: '', license_type: LicenseType.A });
    setEditingId(null);
  };

  return (
    <div>
      <div className="card">
        <h2>{editingId ? 'Edit Driver' : 'Add New Driver'}</h2>

        {error && <div className="error-message">{error}</div>}
        {successMessage && <div className="success-message">{successMessage}</div>}

        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="driver-name">Name</label>
            <input
              id="driver-name"
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              placeholder="Enter driver name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="driver-license">License Type</label>
            <select
              id="driver-license"
              value={formData.license_type}
              onChange={(e) =>
                setFormData({ ...formData, license_type: e.target.value as LicenseType })
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
              {editingId ? 'Update Driver' : 'Create Driver'}
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
        <h2>Drivers List</h2>

        {loading ? (
          <div className="loading">Loading drivers...</div>
        ) : drivers.length === 0 ? (
          <div className="empty-state">No drivers found. Create one above!</div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>License Type</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {drivers.map((driver) => (
                  <tr key={driver.id}>
                    <td>{driver.id}</td>
                    <td>{driver.name}</td>
                    <td>{driver.license_type}</td>
                    <td>
                      <div className="table-actions">
                        <button
                          className="btn btn-primary btn-small"
                          onClick={() => handleEdit(driver)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-danger btn-small"
                          onClick={() => handleDelete(driver.id)}
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
