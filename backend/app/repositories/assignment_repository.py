"""
Assignment repository for data persistence operations.
Implements the Repository Pattern to separate business logic from data access.
"""
from typing import List, Optional
from datetime import date
from app.models.assignment import Assignment


class AssignmentRepository:
    """
    Handles data persistence for Assignment entities.
    Uses in-memory storage for simplicity (can be replaced with actual database).
    """

    def __init__(self):
        """Initialize the repository with empty storage"""
        self._assignments: dict[int, Assignment] = {}
        self._next_id: int = 1

    def create(self, assignment: Assignment) -> Assignment:
        """
        Creates a new assignment in the repository.

        Args:
            assignment: Assignment entity to create

        Returns:
            Assignment: The created assignment with assigned ID
        """
        assignment.id = self._next_id
        self._assignments[self._next_id] = assignment
        self._next_id += 1
        return assignment

    def get_by_id(self, assignment_id: int) -> Optional[Assignment]:
        """
        Retrieves an assignment by its ID.

        Args:
            assignment_id: The assignment's unique identifier

        Returns:
            Optional[Assignment]: The assignment if found, None otherwise
        """
        return self._assignments.get(assignment_id)

    def get_all(self) -> List[Assignment]:
        """
        Retrieves all assignments.

        Returns:
            List[Assignment]: List of all assignments
        """
        return list(self._assignments.values())

    def update(self, assignment_id: int, assignment: Assignment) -> Optional[Assignment]:
        """
        Updates an existing assignment.

        Args:
            assignment_id: The assignment's unique identifier
            assignment: Assignment entity with updated data

        Returns:
            Optional[Assignment]: The updated assignment if found, None otherwise
        """
        if assignment_id not in self._assignments:
            return None

        assignment.id = assignment_id
        self._assignments[assignment_id] = assignment
        return assignment

    def delete(self, assignment_id: int) -> bool:
        """
        Deletes an assignment from the repository.

        Args:
            assignment_id: The assignment's unique identifier

        Returns:
            bool: True if assignment was deleted, False if not found
        """
        if assignment_id in self._assignments:
            del self._assignments[assignment_id]
            return True
        return False

    def find_by_driver_and_date(self, driver_id: int, assignment_date: date) -> Optional[Assignment]:
        """
        Finds an assignment for a specific driver on a specific date.

        Args:
            driver_id: The driver's ID
            assignment_date: The date to check

        Returns:
            Optional[Assignment]: The assignment if found, None otherwise
        """
        for assignment in self._assignments.values():
            if (assignment.driver_id == driver_id and
                assignment.assignment_date == assignment_date):
                return assignment
        return None

    def find_by_truck_and_date(self, truck_id: int, assignment_date: date) -> Optional[Assignment]:
        """
        Finds an assignment for a specific truck on a specific date.

        Args:
            truck_id: The truck's ID
            assignment_date: The date to check

        Returns:
            Optional[Assignment]: The assignment if found, None otherwise
        """
        for assignment in self._assignments.values():
            if (assignment.truck_id == truck_id and
                assignment.assignment_date == assignment_date):
                return assignment
        return None

    def find_by_date(self, assignment_date: date) -> List[Assignment]:
        """
        Finds all assignments for a specific date.

        Args:
            assignment_date: The date to search

        Returns:
            List[Assignment]: List of assignments on that date
        """
        return [
            assignment
            for assignment in self._assignments.values()
            if assignment.assignment_date == assignment_date
        ]
