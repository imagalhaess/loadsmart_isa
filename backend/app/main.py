"""
Main FastAPI application.
Configures the API with CORS, routes, and exception handlers.
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import driver_routes, truck_routes, assignment_routes
from app.exceptions import ApplicationException


# Create FastAPI application
app = FastAPI(
    title="Truck & Driver Management System",
    description="API for managing trucks, drivers, and their assignments",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for application exceptions
@app.exception_handler(ApplicationException)
async def application_exception_handler(request: Request, exc: ApplicationException):
    """
    Handles all application-specific exceptions.

    Args:
        request: The HTTP request
        exc: The application exception

    Returns:
        JSONResponse: Error response with appropriate status code
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# Include routers
app.include_router(driver_routes.router, prefix="/api")
app.include_router(truck_routes.router, prefix="/api")
app.include_router(assignment_routes.router, prefix="/api")


# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "truck-driver-management"}


# Root endpoint
@app.get("/", tags=["root"])
def root():
    """
    Root endpoint with API information.

    Returns:
        dict: API information
    """
    return {
        "message": "Truck & Driver Management API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
