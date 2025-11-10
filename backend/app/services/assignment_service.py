"""
Assignment service containing business logic for driver-truck assignments.
Implements complex business rules and validations.
"""
from typing import List
from datetime import date
from app.models.assignment import Assignment
from app.models.license_type import LicenseType
from app.repositories.assignment_repository import AssignmentRepository
from app.repositories.driver_repository import DriverRepository
from app.repositories.truck_repository import TruckRepository
from app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    ConflictException
)


class AssignmentService:
    """
    Service layer for assignment-related business operations.
    Implements business rules for driver-truck assignments.
    """

    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        driver_repository: DriverRepository,
        truck_repository: TruckRepository
    ):
        """
        Initialize the service with its dependencies.

        Args:
            assignment_repository: Assignment repository for data access
            driver_repository: Driver repository for validation
            truck_repository: Truck repository for validation
        """
        self._assignment_repo = assignment_repository
        self._driver_repo = driver_repository
        self._truck_repo = truck_repository

    def create_assignment(self, assignment: Assignment) -> Assignment:
        """
        Creates a new driver-truck assignment with full validation.

        Args:
            assignment: Assignment entity to create

        Returns:
            Assignment: The created assignment with assigned ID

        Raises:
            ResourceNotFoundException: If driver or truck doesn't exist
            ValidationException: If license compatibility fails
            ConflictException: If driver or truck is already assigned on that date
        """
        # Validate that driver exists
        driver = self._driver_repo.get_by_id(assignment.driver_id)
        if not driver:
            raise ResourceNotFoundException("Driver", assignment.driver_id)

        # Validate that truck exists
        truck = self._truck_repo.get_by_id(assignment.truck_id)
        if not truck:
            raise ResourceNotFoundException("Truck", assignment.truck_id)

        # Validate license compatibility
        self._validate_license_compatibility(driver.license_type, truck.minimum_license_type)

        # Check for driver conflicts on the same date
        self._check_driver_availability(assignment.driver_id, assignment.assignment_date)

        # Check for truck conflicts on the same date
        self._check_truck_availability(assignment.truck_id, assignment.assignment_date)

        # If all validations pass, create the assignment
        return self._assignment_repo.create(assignment)

    def get_assignment(self, assignment_id: int) -> Assignment:
        """
        Retrieves an assignment by ID.

        Args:
            assignment_id: The assignment's unique identifier

        Returns:
            Assignment: The requested assignment

        Raises:
            ResourceNotFoundException: If assignment is not found
        """
        assignment = self._assignment_repo.get_by_id(assignment_id)
        if not assignment:
            raise ResourceNotFoundException("Assignment", assignment_id)
        return assignment

    def get_all_assignments(self) -> List[Assignment]:
        """
        Retrieves all assignments.

        Returns:
            List[Assignment]: List of all assignments
        """
        return self._assignment_repo.get_all()

    def get_assignments_by_date(self, assignment_date: date) -> List[Assignment]:
        """
        Retrieves all assignments for a specific date.

        Args:
            assignment_date: The date to filter by

        Returns:
            List[Assignment]: List of assignments on that date
        """
        return self._assignment_repo.find_by_date(assignment_date)

    def update_assignment(self, assignment_id: int, assignment: Assignment) -> Assignment:
        """
        Updates an existing assignment with full validation.

        Args:
            assignment_id: The assignment's unique identifier
            assignment: Assignment entity with updated data

        Returns:
            Assignment: The updated assignment

        Raises:
            ResourceNotFoundException: If assignment, driver, or truck doesn't exist
            ValidationException: If license compatibility fails
            ConflictException: If driver or truck is already assigned on that date
        """
        # Check if assignment exists
        existing_assignment = self._assignment_repo.get_by_id(assignment_id)
        if not existing_assignment:
            raise ResourceNotFoundException("Assignment", assignment_id)

        # Validate that driver exists
        driver = self._driver_repo.get_by_id(assignment.driver_id)
        if not driver:
            raise ResourceNotFoundException("Driver", assignment.driver_id)

        # Validate that truck exists
        truck = self._truck_repo.get_by_id(assignment.truck_id)
        if not truck:
            raise ResourceNotFoundException("Truck", assignment.truck_id)

        # Validate license compatibility
        self._validate_license_compatibility(driver.license_type, truck.minimum_license_type)

        # Check for driver conflicts (excluding current assignment)
        self._check_driver_availability(
            assignment.driver_id,
            assignment.assignment_date,
            exclude_assignment_id=assignment_id
        )

        # Check for truck conflicts (excluding current assignment)
        self._check_truck_availability(
            assignment.truck_id,
            assignment.assignment_date,
            exclude_assignment_id=assignment_id
        )

        # If all validations pass, update the assignment
        return self._assignment_repo.update(assignment_id, assignment)

    def delete_assignment(self, assignment_id: int) -> None:
        """
        Deletes an assignment.

        Args:
            assignment_id: The assignment's unique identifier

        Raises:
            ResourceNotFoundException: If assignment is not found
        """
        deleted = self._assignment_repo.delete(assignment_id)
        if not deleted:
            raise ResourceNotFoundException("Assignment", assignment_id)

    def _validate_license_compatibility(
        self,
        driver_license: LicenseType,
        required_license: LicenseType
    ) -> None:
        """
        Validates if driver's license is compatible with truck's requirements.

        Args:
            driver_license: The driver's license type
            required_license: The minimum license required for the truck

        Raises:
            ValidationException: If license is incompatible
        """
        if not driver_license.can_operate(required_license):
            raise ValidationException(
                f"Driver with license type {driver_license.value} cannot operate "
                f"a truck requiring license type {required_license.value}. "
                f"Driver needs at least a {required_license.value} license."
            )

    def _check_driver_availability(
        self,
        driver_id: int,
        assignment_date: date,
        exclude_assignment_id: int = None
    ) -> None:
        """
        Checks if a driver is available on a specific date.

        Args:
            driver_id: The driver's ID
            assignment_date: The date to check
            exclude_assignment_id: Optional assignment ID to exclude from check (for updates)

        Raises:
            ConflictException: If driver is already assigned on that date
        """
        existing = self._assignment_repo.find_by_driver_and_date(driver_id, assignment_date)
        if existing and existing.id != exclude_assignment_id:
            raise ConflictException(
                f"Driver {driver_id} is already assigned to truck {existing.truck_id} "
                f"on {assignment_date}"
            )

    def _check_truck_availability(
        self,
        truck_id: int,
        assignment_date: date,
        exclude_assignment_id: int = None
    ) -> None:
        """
        Checks if a truck is available on a specific date.

        Args:
            truck_id: The truck's ID
            assignment_date: The date to check
            exclude_assignment_id: Optional assignment ID to exclude from check (for updates)

        Raises:
            ConflictException: If truck is already assigned on that date
        """
        existing = self._assignment_repo.find_by_truck_and_date(truck_id, assignment_date)
        if existing and existing.id != exclude_assignment_id:
            raise ConflictException(
                f"Truck {truck_id} is already assigned to driver {existing.driver_id} "
                f"on {assignment_date}"
            )
