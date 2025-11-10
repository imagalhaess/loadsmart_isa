"""
Driver repository for data persistence operations.
Implements the Repository Pattern to separate business logic from data access.
"""
from typing import List, Optional
from app.models.driver import Driver


class DriverRepository:
    """
    Handles data persistence for Driver entities.
    Uses in-memory storage for simplicity (can be replaced with actual database).
    """

    def __init__(self):
        """Initialize the repository with empty storage"""
        self._drivers: dict[int, Driver] = {}
        self._next_id: int = 1

    def create(self, driver: Driver) -> Driver:
        """
        Creates a new driver in the repository.

        Args:
            driver: Driver entity to create

        Returns:
            Driver: The created driver with assigned ID
        """
        driver.id = self._next_id
        self._drivers[self._next_id] = driver
        self._next_id += 1
        return driver

    def get_by_id(self, driver_id: int) -> Optional[Driver]:
        """
        Retrieves a driver by their ID.

        Args:
            driver_id: The driver's unique identifier

        Returns:
            Optional[Driver]: The driver if found, None otherwise
        """
        return self._drivers.get(driver_id)

    def get_all(self) -> List[Driver]:
        """
        Retrieves all drivers.

        Returns:
            List[Driver]: List of all drivers
        """
        return list(self._drivers.values())

    def update(self, driver_id: int, driver: Driver) -> Optional[Driver]:
        """
        Updates an existing driver.

        Args:
            driver_id: The driver's unique identifier
            driver: Driver entity with updated data

        Returns:
            Optional[Driver]: The updated driver if found, None otherwise
        """
        if driver_id not in self._drivers:
            return None

        driver.id = driver_id
        self._drivers[driver_id] = driver
        return driver

    def delete(self, driver_id: int) -> bool:
        """
        Deletes a driver from the repository.

        Args:
            driver_id: The driver's unique identifier

        Returns:
            bool: True if driver was deleted, False if not found
        """
        if driver_id in self._drivers:
            del self._drivers[driver_id]
            return True
        return False

    def exists(self, driver_id: int) -> bool:
        """
        Checks if a driver exists in the repository.

        Args:
            driver_id: The driver's unique identifier

        Returns:
            bool: True if driver exists, False otherwise
        """
        return driver_id in self._drivers
