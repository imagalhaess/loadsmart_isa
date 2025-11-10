"""
Truck repository for data persistence operations.
Implements the Repository Pattern to separate business logic from data access.
"""
from typing import List, Optional
from app.models.truck import Truck


class TruckRepository:
    """
    Handles data persistence for Truck entities.
    Uses in-memory storage for simplicity (can be replaced with actual database).
    """

    def __init__(self):
        """Initialize the repository with empty storage"""
        self._trucks: dict[int, Truck] = {}
        self._next_id: int = 1

    def create(self, truck: Truck) -> Truck:
        """
        Creates a new truck in the repository.

        Args:
            truck: Truck entity to create

        Returns:
            Truck: The created truck with assigned ID
        """
        truck.id = self._next_id
        self._trucks[self._next_id] = truck
        self._next_id += 1
        return truck

    def get_by_id(self, truck_id: int) -> Optional[Truck]:
        """
        Retrieves a truck by its ID.

        Args:
            truck_id: The truck's unique identifier

        Returns:
            Optional[Truck]: The truck if found, None otherwise
        """
        return self._trucks.get(truck_id)

    def get_all(self) -> List[Truck]:
        """
        Retrieves all trucks.

        Returns:
            List[Truck]: List of all trucks
        """
        return list(self._trucks.values())

    def update(self, truck_id: int, truck: Truck) -> Optional[Truck]:
        """
        Updates an existing truck.

        Args:
            truck_id: The truck's unique identifier
            truck: Truck entity with updated data

        Returns:
            Optional[Truck]: The updated truck if found, None otherwise
        """
        if truck_id not in self._trucks:
            return None

        truck.id = truck_id
        self._trucks[truck_id] = truck
        return truck

    def delete(self, truck_id: int) -> bool:
        """
        Deletes a truck from the repository.

        Args:
            truck_id: The truck's unique identifier

        Returns:
            bool: True if truck was deleted, False if not found
        """
        if truck_id in self._trucks:
            del self._trucks[truck_id]
            return True
        return False

    def exists(self, truck_id: int) -> bool:
        """
        Checks if a truck exists in the repository.

        Args:
            truck_id: The truck's unique identifier

        Returns:
            bool: True if truck exists, False otherwise
        """
        return truck_id in self._trucks
