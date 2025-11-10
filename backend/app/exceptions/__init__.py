"""
Custom exceptions for the application.
Following the Single Responsibility Principle - each exception has a specific purpose.
"""


class ApplicationException(Exception):
    """Base exception for all application errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(ApplicationException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource_type: str, resource_id: int):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, status_code=404)


class ValidationException(ApplicationException):
    """Raised when business validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class ConflictException(ApplicationException):
    """Raised when there's a conflict with existing data"""
    def __init__(self, message: str):
        super().__init__(message, status_code=409)
