# Quick Start Guide

This guide will help you get the Truck & Driver Management System up and running in just a few minutes.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** (check with `python3 --version`)
- **Node.js 18+** (check with `node --version`)
- **npm** or **yarn** (check with `npm --version`)

## Step-by-Step Setup

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python3 -m uvicorn app.main:app --reload
```

The backend API will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/api/docs`
- Alternative Docs: `http://localhost:8000/api/redoc`

### 2. Frontend Setup (3 minutes)

Open a **new terminal window** (keep the backend running) and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend application will be available at: `http://localhost:5173`

### 3. Testing the Application

#### Manual Testing
1. Open your browser and navigate to `http://localhost:5173`
2. Start by creating a few drivers with different license types
3. Create some trucks with different minimum license requirements
4. Try creating assignments and test the validation rules

#### Running Automated Tests

Backend tests:
```bash
cd backend
pytest
```

For test coverage report:
```bash
pytest --cov=app tests/
```

## Key Features to Test

### License Hierarchy
The system implements this hierarchy: **E > D > C > B > A**
- A driver with license **D** can operate trucks requiring **D, C, B, or A**
- A driver with license **B** cannot operate trucks requiring **C, D, or E**

### Validation Rules
Try these scenarios to see validation in action:

1. **License Compatibility**: Try assigning a driver with license type B to a truck requiring license type D (should fail)

2. **Driver Double-Booking**: Create an assignment for a driver on a specific date, then try to assign the same driver to another truck on the same date (should fail)

3. **Truck Double-Booking**: Create an assignment for a truck on a specific date, then try to assign another driver to the same truck on the same date (should fail)

4. **Valid Assignment**: Assign a driver with license type D to a truck requiring license type C on any date (should succeed)

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
# Or manually specify a different port
uvicorn app.main:app --reload --port 8001
```

**Import errors:**
Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Frontend Issues

**Port 5173 already in use:**
The Vite dev server will automatically try the next available port (5174, 5175, etc.)

**API connection errors:**
1. Ensure the backend is running on `http://localhost:8000`
2. Check the `.env` file exists (copy from `.env.example` if needed)
3. Verify CORS is configured correctly in the backend

## Project Structure

```
loadsmart/
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── models/       # Domain models (Driver, Truck, Assignment)
│   │   ├── repositories/ # Data access layer
│   │   ├── services/     # Business logic
│   │   ├── routes/       # API endpoints
│   │   ├── schemas/      # Request/Response validation
│   │   └── main.py       # Application entry point
│   └── tests/            # Automated tests
│
└── frontend/             # React + TypeScript frontend
    ├── src/
    │   ├── components/   # React components
    │   ├── hooks/        # Custom React hooks
    │   ├── services/     # API communication
    │   └── types/        # TypeScript type definitions
    └── package.json

```

## Architecture Highlights

### Backend (Python + FastAPI)
- **Clean Architecture**: Separation of concerns with layers (routes → services → repositories → models)
- **SOLID Principles**: Each service has a single responsibility, dependency injection throughout
- **Repository Pattern**: Abstracted data access (easy to swap in-memory for database)
- **Comprehensive Validation**: License compatibility, double-booking prevention, resource existence checks

### Frontend (React + TypeScript)
- **Component-Based**: Modular, reusable components
- **Custom Hooks**: Encapsulated state management and API calls
- **Type Safety**: Full TypeScript coverage for compile-time error detection
- **User-Friendly**: Clear error messages, success feedback, loading states

## API Endpoints

### Drivers
- `GET /api/drivers` - List all drivers
- `POST /api/drivers` - Create a new driver
- `PUT /api/drivers/{id}` - Update a driver
- `DELETE /api/drivers/{id}` - Delete a driver

### Trucks
- `GET /api/trucks` - List all trucks
- `POST /api/trucks` - Create a new truck
- `PUT /api/trucks/{id}` - Update a truck
- `DELETE /api/trucks/{id}` - Delete a truck

### Assignments
- `GET /api/assignments` - List all assignments (supports `?assignment_date=YYYY-MM-DD` filter)
- `POST /api/assignments` - Create a new assignment (with validation)
- `PUT /api/assignments/{id}` - Update an assignment (with validation)
- `DELETE /api/assignments/{id}` - Delete an assignment

## Development Notes

### Code Quality
- Well-documented code with docstrings (Python) and JSDoc comments (TypeScript)
- Consistent naming conventions throughout
- Comprehensive error handling with appropriate HTTP status codes
- Clean separation of concerns

### Testing
- Backend: 28 automated tests covering critical business logic
- License hierarchy validation tests
- Assignment service validation tests
- Integration tests for all API endpoints

### Future Enhancements
For a production-ready version, consider:
- Database integration (PostgreSQL/MySQL)
- User authentication and authorization
- Pagination for large datasets
- Advanced search and filtering
- Export functionality (PDF, Excel)
- Email notifications
- Audit logging
- Mobile-responsive design improvements

## Need Help?

- Check the main **README.md** for detailed documentation
- Review the API docs at `http://localhost:8000/api/docs` when the backend is running
- Look at the test files in `backend/tests/` for usage examples

## License

This project was created as a technical assessment for Loadsmart.
