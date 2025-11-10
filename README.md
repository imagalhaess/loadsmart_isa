# Truck & Driver Management System

A fullstack web application for managing trucks, drivers, and their assignments. Built with React (TypeScript) on the frontend and FastAPI (Python) on the backend.

## Features

- **Driver Management**: Create, view, update, and delete drivers with license type tracking
- **Truck Management**: Manage trucks with license requirements
- **Assignment Management**: Assign drivers to trucks with comprehensive validation:
  - License compatibility checking
  - Conflict detection (no double bookings)
  - Date-based filtering
  - Real-time validation feedback

## Tech Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **Pydantic**: Data validation and settings management
- **Python 3.8+**: Core programming language
- **Pytest**: Testing framework

### Frontend
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **Axios**: HTTP client

## Architecture

The project follows **SOLID principles** and clean architecture patterns:

### Backend Structure
```
backend/
├── app/
│   ├── models/          # Domain models (Driver, Truck, Assignment, LicenseType)
│   ├── repositories/    # Data access layer (Repository pattern)
│   ├── services/        # Business logic layer
│   ├── routes/          # API endpoints (Controllers)
│   ├── schemas/         # Request/Response validation schemas
│   ├── exceptions/      # Custom exception classes
│   └── main.py          # Application entry point
└── tests/              # Unit and integration tests
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/      # React components
│   ├── hooks/           # Custom React hooks
│   ├── services/        # API communication layer
│   ├── types/           # TypeScript type definitions
│   └── App.tsx          # Main application component
└── package.json
```

## Design Principles

### SOLID Principles Applied

1. **Single Responsibility Principle (SRP)**
   - Each service handles one entity (DriverService, TruckService, AssignmentService)
   - Each repository handles data access for one entity
   - Each component manages one specific UI concern

2. **Open/Closed Principle (OCP)**
   - Services are open for extension but closed for modification
   - New validation rules can be added without changing existing code

3. **Liskov Substitution Principle (LSP)**
   - Repository implementations can be swapped (e.g., in-memory to database)
   - Service interfaces remain consistent

4. **Interface Segregation Principle (ISP)**
   - API schemas are separated from domain models
   - Frontend types are separated from API responses

5. **Dependency Inversion Principle (DIP)**
   - Services depend on repository abstractions
   - Routes depend on service abstractions through dependency injection

### KISS (Keep It Simple, Stupid)

- Clear, readable code with descriptive variable names
- Simple in-memory storage (can be replaced with database)
- Straightforward UI without over-engineering
- Direct API communication without unnecessary abstractions

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`
- Alternative Docs: `http://localhost:8000/api/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Running Tests

### Backend Tests

```bash
cd backend
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## API Endpoints

### Drivers
- `GET /api/drivers` - Get all drivers
- `GET /api/drivers/{id}` - Get driver by ID
- `POST /api/drivers` - Create a new driver
- `PUT /api/drivers/{id}` - Update a driver
- `DELETE /api/drivers/{id}` - Delete a driver

### Trucks
- `GET /api/trucks` - Get all trucks
- `GET /api/trucks/{id}` - Get truck by ID
- `POST /api/trucks` - Create a new truck
- `PUT /api/trucks/{id}` - Update a truck
- `DELETE /api/trucks/{id}` - Delete a truck

### Assignments
- `GET /api/assignments` - Get all assignments (optional date filter)
- `GET /api/assignments/{id}` - Get assignment by ID
- `POST /api/assignments` - Create a new assignment
- `PUT /api/assignments/{id}` - Update an assignment
- `DELETE /api/assignments/{id}` - Delete an assignment

## Business Rules

### License Hierarchy

The system implements a hierarchical license system:

```
E > D > C > B > A
```

- A driver with license type **E** can operate trucks requiring E, D, C, B, or A
- A driver with license type **D** can operate trucks requiring D, C, B, or A
- A driver with license type **C** can operate trucks requiring C, B, or A
- A driver with license type **B** can operate trucks requiring B or A
- A driver with license type **A** can only operate trucks requiring A

### Assignment Validation

The system enforces the following rules when creating or updating assignments:

1. **Driver must exist** in the system
2. **Truck must exist** in the system
3. **License compatibility**: Driver's license must meet or exceed truck's minimum requirement
4. **No double booking for drivers**: A driver cannot be assigned to multiple trucks on the same date
5. **No double booking for trucks**: A truck cannot be assigned to multiple drivers on the same date

## Error Handling

The application provides clear, user-friendly error messages:

- **404 Not Found**: When a resource doesn't exist
- **409 Conflict**: When there's a scheduling conflict
- **422 Validation Error**: When business rules are violated (e.g., license incompatibility)

## Future Enhancements

Potential improvements for production:

- Database integration (PostgreSQL/MySQL)
- User authentication and authorization
- Assignment history and audit logging
- Search and advanced filtering
- Export functionality (PDF, Excel)
- Email notifications for assignments
- Mobile-responsive design improvements
- Real-time updates with WebSockets
- Pagination for large datasets

## License

This project was created as a technical assessment for Loadsmart.

## Contact

For questions or issues, please contact the development team.
