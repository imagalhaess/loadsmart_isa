"""
Unit tests for assignment service.
Tests business logic and validation rules for assignments.
"""
import pytest
from datetime import date
from app.models.driver import Driver
from app.models.truck import Truck
from app.models.assignment import Assignment
from app.models.license_type import LicenseType
from app.repositories.driver_repository import DriverRepository
from app.repositories.truck_repository import TruckRepository
from app.repositories.assignment_repository import AssignmentRepository
from app.services.assignment_service import AssignmentService
from app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    ConflictException
)


class TestAssignmentService:
    """Test suite for AssignmentService"""

    @pytest.fixture
    def service(self):
        """Create a fresh service instance for each test"""
        driver_repo = DriverRepository()
        truck_repo = TruckRepository()
        assignment_repo = AssignmentRepository()
        return AssignmentService(assignment_repo, driver_repo, truck_repo)

    @pytest.fixture
    def driver_with_license_d(self, service):
        """Create a driver with license D"""
        driver = Driver(name="John Doe", license_type=LicenseType.D)
        return service._driver_repo.create(driver)

    @pytest.fixture
    def driver_with_license_b(self, service):
        """Create a driver with license B"""
        driver = Driver(name="Jane Smith", license_type=LicenseType.B)
        return service._driver_repo.create(driver)

    @pytest.fixture
    def truck_requiring_c(self, service):
        """Create a truck requiring license C"""
        truck = Truck(plate="ABC-1234", minimum_license_type=LicenseType.C)
        return service._truck_repo.create(truck)

    @pytest.fixture
    def truck_requiring_b(self, service):
        """Create a truck requiring license B"""
        truck = Truck(plate="XYZ-5678", minimum_license_type=LicenseType.B)
        return service._truck_repo.create(truck)

    def test_create_assignment_success(
        self,
        service,
        driver_with_license_d,
        truck_requiring_c
    ):
        """Test successful assignment creation"""
        assignment = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )

        created = service.create_assignment(assignment)

        assert created.id is not None
        assert created.driver_id == driver_with_license_d.id
        assert created.truck_id == truck_requiring_c.id
        assert created.assignment_date == date(2025, 11, 10)

    def test_create_assignment_driver_not_found(self, service, truck_requiring_c):
        """Test assignment creation with non-existent driver"""
        assignment = Assignment(
            driver_id=999,  # Non-existent driver
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )

        with pytest.raises(ResourceNotFoundException) as exc_info:
            service.create_assignment(assignment)

        assert "Driver" in str(exc_info.value.message)
        assert "999" in str(exc_info.value.message)

    def test_create_assignment_truck_not_found(self, service, driver_with_license_d):
        """Test assignment creation with non-existent truck"""
        assignment = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=999,  # Non-existent truck
            assignment_date=date(2025, 11, 10)
        )

        with pytest.raises(ResourceNotFoundException) as exc_info:
            service.create_assignment(assignment)

        assert "Truck" in str(exc_info.value.message)
        assert "999" in str(exc_info.value.message)

    def test_create_assignment_incompatible_license(
        self,
        service,
        driver_with_license_b,
        truck_requiring_c
    ):
        """Test assignment creation with incompatible license"""
        assignment = Assignment(
            driver_id=driver_with_license_b.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )

        with pytest.raises(ValidationException) as exc_info:
            service.create_assignment(assignment)

        assert "license type B" in str(exc_info.value.message)
        assert "license type C" in str(exc_info.value.message)

    def test_create_assignment_driver_already_assigned(
        self,
        service,
        driver_with_license_d,
        truck_requiring_c,
        truck_requiring_b
    ):
        """Test that a driver cannot be assigned to multiple trucks on the same day"""
        # Create first assignment
        assignment1 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )
        service.create_assignment(assignment1)

        # Try to create second assignment for same driver on same date
        assignment2 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_b.id,
            assignment_date=date(2025, 11, 10)
        )

        with pytest.raises(ConflictException) as exc_info:
            service.create_assignment(assignment2)

        assert "already assigned" in str(exc_info.value.message)

    def test_create_assignment_truck_already_assigned(
        self,
        service,
        driver_with_license_d,
        driver_with_license_b,
        truck_requiring_b
    ):
        """Test that a truck cannot be assigned to multiple drivers on the same day"""
        # Create first assignment
        assignment1 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_b.id,
            assignment_date=date(2025, 11, 10)
        )
        service.create_assignment(assignment1)

        # Try to create second assignment for same truck on same date
        assignment2 = Assignment(
            driver_id=driver_with_license_b.id,
            truck_id=truck_requiring_b.id,
            assignment_date=date(2025, 11, 10)
        )

        with pytest.raises(ConflictException) as exc_info:
            service.create_assignment(assignment2)

        assert "already assigned" in str(exc_info.value.message)

    def test_create_assignment_same_day_different_date_allowed(
        self,
        service,
        driver_with_license_d,
        truck_requiring_c
    ):
        """Test that same driver and truck can be assigned on different dates"""
        # Create assignment for Nov 10
        assignment1 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )
        service.create_assignment(assignment1)

        # Create assignment for Nov 11 - should succeed
        assignment2 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 11)
        )
        created = service.create_assignment(assignment2)

        assert created.id is not None

    def test_get_all_assignments(
        self,
        service,
        driver_with_license_d,
        truck_requiring_c
    ):
        """Test retrieving all assignments"""
        assignment1 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )
        assignment2 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 11)
        )

        service.create_assignment(assignment1)
        service.create_assignment(assignment2)

        all_assignments = service.get_all_assignments()
        assert len(all_assignments) == 2

    def test_get_assignments_by_date(
        self,
        service,
        driver_with_license_d,
        truck_requiring_c
    ):
        """Test retrieving assignments filtered by date"""
        date1 = date(2025, 11, 10)
        date2 = date(2025, 11, 11)

        assignment1 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date1
        )
        assignment2 = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date2
        )

        service.create_assignment(assignment1)
        service.create_assignment(assignment2)

        assignments_date1 = service.get_assignments_by_date(date1)
        assert len(assignments_date1) == 1
        assert assignments_date1[0].assignment_date == date1

    def test_delete_assignment(
        self,
        service,
        driver_with_license_d,
        truck_requiring_c
    ):
        """Test deleting an assignment"""
        assignment = Assignment(
            driver_id=driver_with_license_d.id,
            truck_id=truck_requiring_c.id,
            assignment_date=date(2025, 11, 10)
        )
        created = service.create_assignment(assignment)

        service.delete_assignment(created.id)

        with pytest.raises(ResourceNotFoundException):
            service.get_assignment(created.id)
