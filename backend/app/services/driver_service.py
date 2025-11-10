"""
Driver service containing business logic for driver management.
Implements the Single Responsibility Principle - handles only driver-related operations.
"""
from typing import List
from app.models.driver import Driver
from app.repositories.driver_repository import DriverRepository
from app.exceptions import ResourceNotFoundException


class DriverService:
    """
    Service layer for driver-related business operations.
    Depends on abstractions (repository), following Dependency Inversion Principle.
    """

    def __init__(self, repository: DriverRepository):
        """
        Initialize the service with its dependency.

        Args:
            repository: Driver repository for data access
        """
        self._repository = repository

    def create_driver(self, driver: Driver) -> Driver:
        """
        Creates a new driver.

        Args:
            driver: Driver entity to create

        Returns:
            Driver: The created driver with assigned ID
        """
        return self._repository.create(driver)

    def get_driver(self, driver_id: int) -> Driver:
        """
        Retrieves a driver by ID.

        Args:
            driver_id: The driver's unique identifier

        Returns:
            Driver: The requested driver

        Raises:
            ResourceNotFoundException: If driver is not found
        """
        driver = self._repository.get_by_id(driver_id)
        if not driver:
            raise ResourceNotFoundException("Driver", driver_id)
        return driver

    def get_all_drivers(self) -> List[Driver]:
        """
        Retrieves all drivers.

        Returns:
            List[Driver]: List of all drivers
        """
        return self._repository.get_all()

    def update_driver(self, driver_id: int, driver: Driver) -> Driver:
        """
        Updates an existing driver.

        Args:
            driver_id: The driver's unique identifier
            driver: Driver entity with updated data

        Returns:
            Driver: The updated driver

        Raises:
            ResourceNotFoundException: If driver is not found
        """
        updated_driver = self._repository.update(driver_id, driver)
        if not updated_driver:
            raise ResourceNotFoundException("Driver", driver_id)
        return updated_driver

    def delete_driver(self, driver_id: int) -> None:
        """
        Deletes a driver.

        Args:
            driver_id: The driver's unique identifier

        Raises:
            ResourceNotFoundException: If driver is not found
        """
        deleted = self._repository.delete(driver_id)
        if not deleted:
            raise ResourceNotFoundException("Driver", driver_id)
