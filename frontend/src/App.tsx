/**
 * Main Application Component
 * Provides tab navigation between different management views.
 */
import { useState } from 'react';
import { DriverManagement } from './components/DriverManagement';
import { TruckManagement } from './components/TruckManagement';
import { AssignmentManagement } from './components/AssignmentManagement';

type Tab = 'drivers' | 'trucks' | 'assignments';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('drivers');

  return (
    <div>
      <header className="header">
        <div className="container">
          <h1>Truck & Driver Management System</h1>
        </div>
      </header>

      <div className="container">
        <nav className="tabs">
          <button
            className={`tab ${activeTab === 'drivers' ? 'active' : ''}`}
            onClick={() => setActiveTab('drivers')}
          >
            Drivers
          </button>
          <button
            className={`tab ${activeTab === 'trucks' ? 'active' : ''}`}
            onClick={() => setActiveTab('trucks')}
          >
            Trucks
          </button>
          <button
            className={`tab ${activeTab === 'assignments' ? 'active' : ''}`}
            onClick={() => setActiveTab('assignments')}
          >
            Assignments
          </button>
        </nav>

        <div className="tab-content">
          {activeTab === 'drivers' && <DriverManagement />}
          {activeTab === 'trucks' && <TruckManagement />}
          {activeTab === 'assignments' && <AssignmentManagement />}
        </div>
      </div>
    </div>
  );
}

export default App;
