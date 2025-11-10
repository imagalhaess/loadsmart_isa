"""
Dependency injection container.
Centralizes service instantiation following Dependency Inversion Principle.
"""
from app.repositories.driver_repository import DriverRepository
from app.repositories.truck_repository import TruckRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.services.driver_service import DriverService
from app.services.truck_service import TruckService
from app.services.assignment_service import AssignmentService


# Singleton repositories (in-memory storage)
_driver_repository = DriverRepository()
_truck_repository = TruckRepository()
_assignment_repository = AssignmentRepository()


def get_driver_service() -> DriverService:
    """
    Returns a DriverService instance with its dependencies.

    Returns:
        DriverService: Driver service instance
    """
    return DriverService(_driver_repository)


def get_truck_service() -> TruckService:
    """
    Returns a TruckService instance with its dependencies.

    Returns:
        TruckService: Truck service instance
    """
    return TruckService(_truck_repository)


def get_assignment_service() -> AssignmentService:
    """
    Returns an AssignmentService instance with its dependencies.

    Returns:
        AssignmentService: Assignment service instance
    """
    return AssignmentService(
        _assignment_repository,
        _driver_repository,
        _truck_repository
    )
