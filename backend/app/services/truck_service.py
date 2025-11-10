"""
Truck service containing business logic for truck management.
Implements the Single Responsibility Principle - handles only truck-related operations.
"""
from typing import List
from app.models.truck import Truck
from app.repositories.truck_repository import TruckRepository
from app.exceptions import ResourceNotFoundException


class TruckService:
    """
    Service layer for truck-related business operations.
    Depends on abstractions (repository), following Dependency Inversion Principle.
    """

    def __init__(self, repository: TruckRepository):
        """
        Initialize the service with its dependency.

        Args:
            repository: Truck repository for data access
        """
        self._repository = repository

    def create_truck(self, truck: Truck) -> Truck:
        """
        Creates a new truck.

        Args:
            truck: Truck entity to create

        Returns:
            Truck: The created truck with assigned ID
        """
        return self._repository.create(truck)

    def get_truck(self, truck_id: int) -> Truck:
        """
        Retrieves a truck by ID.

        Args:
            truck_id: The truck's unique identifier

        Returns:
            Truck: The requested truck

        Raises:
            ResourceNotFoundException: If truck is not found
        """
        truck = self._repository.get_by_id(truck_id)
        if not truck:
            raise ResourceNotFoundException("Truck", truck_id)
        return truck

    def get_all_trucks(self) -> List[Truck]:
        """
        Retrieves all trucks.

        Returns:
            List[Truck]: List of all trucks
        """
        return self._repository.get_all()

    def update_truck(self, truck_id: int, truck: Truck) -> Truck:
        """
        Updates an existing truck.

        Args:
            truck_id: The truck's unique identifier
            truck: Truck entity with updated data

        Returns:
            Truck: The updated truck

        Raises:
            ResourceNotFoundException: If truck is not found
        """
        updated_truck = self._repository.update(truck_id, truck)
        if not updated_truck:
            raise ResourceNotFoundException("Truck", truck_id)
        return updated_truck

    def delete_truck(self, truck_id: int) -> None:
        """
        Deletes a truck.

        Args:
            truck_id: The truck's unique identifier

        Raises:
            ResourceNotFoundException: If truck is not found
        """
        deleted = self._repository.delete(truck_id)
        if not deleted:
            raise ResourceNotFoundException("Truck", truck_id)
