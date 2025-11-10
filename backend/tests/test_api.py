"""
Integration tests for the API endpoints.
Tests the complete request/response cycle.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestDriverAPI:
    """Test suite for driver API endpoints"""

    def test_create_driver(self):
        """Test creating a new driver"""
        response = client.post(
            "/api/drivers",
            json={"name": "John Doe", "license_type": "D"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["license_type"] == "D"
        assert "id" in data

    def test_get_all_drivers(self):
        """Test retrieving all drivers"""
        # Create a driver first
        client.post(
            "/api/drivers",
            json={"name": "Jane Smith", "license_type": "C"}
        )

        response = client.get("/api/drivers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_driver_by_id(self):
        """Test retrieving a specific driver"""
        # Create a driver
        create_response = client.post(
            "/api/drivers",
            json={"name": "Bob Johnson", "license_type": "B"}
        )
        driver_id = create_response.json()["id"]

        # Get the driver
        response = client.get(f"/api/drivers/{driver_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == driver_id
        assert data["name"] == "Bob Johnson"

    def test_get_driver_not_found(self):
        """Test retrieving a non-existent driver"""
        response = client.get("/api/drivers/99999")
        assert response.status_code == 404

    def test_update_driver(self):
        """Test updating a driver"""
        # Create a driver
        create_response = client.post(
            "/api/drivers",
            json={"name": "Alice Brown", "license_type": "A"}
        )
        driver_id = create_response.json()["id"]

        # Update the driver
        response = client.put(
            f"/api/drivers/{driver_id}",
            json={"name": "Alice Brown-Smith", "license_type": "C"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Alice Brown-Smith"
        assert data["license_type"] == "C"

    def test_delete_driver(self):
        """Test deleting a driver"""
        # Create a driver
        create_response = client.post(
            "/api/drivers",
            json={"name": "Charlie Davis", "license_type": "E"}
        )
        driver_id = create_response.json()["id"]

        # Delete the driver
        response = client.delete(f"/api/drivers/{driver_id}")
        assert response.status_code == 204

        # Verify driver is deleted
        get_response = client.get(f"/api/drivers/{driver_id}")
        assert get_response.status_code == 404


class TestTruckAPI:
    """Test suite for truck API endpoints"""

    def test_create_truck(self):
        """Test creating a new truck"""
        response = client.post(
            "/api/trucks",
            json={"plate": "ABC-1234", "minimum_license_type": "C"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["plate"] == "ABC-1234"
        assert data["minimum_license_type"] == "C"
        assert "id" in data

    def test_get_all_trucks(self):
        """Test retrieving all trucks"""
        # Create a truck first
        client.post(
            "/api/trucks",
            json={"plate": "XYZ-5678", "minimum_license_type": "D"}
        )

        response = client.get("/api/trucks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestAssignmentAPI:
    """Test suite for assignment API endpoints"""

    def test_create_assignment_success(self):
        """Test creating a valid assignment"""
        # Create driver with license D
        driver_response = client.post(
            "/api/drivers",
            json={"name": "Driver Test", "license_type": "D"}
        )
        driver_id = driver_response.json()["id"]

        # Create truck requiring license C
        truck_response = client.post(
            "/api/trucks",
            json={"plate": "TEST-123", "minimum_license_type": "C"}
        )
        truck_id = truck_response.json()["id"]

        # Create assignment
        response = client.post(
            "/api/assignments",
            json={
                "driver_id": driver_id,
                "truck_id": truck_id,
                "assignment_date": "2025-11-10"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["driver_id"] == driver_id
        assert data["truck_id"] == truck_id
        assert data["assignment_date"] == "2025-11-10"

    def test_create_assignment_incompatible_license(self):
        """Test creating assignment with incompatible license"""
        # Create driver with license B
        driver_response = client.post(
            "/api/drivers",
            json={"name": "Low License Driver", "license_type": "B"}
        )
        driver_id = driver_response.json()["id"]

        # Create truck requiring license D
        truck_response = client.post(
            "/api/trucks",
            json={"plate": "HIGH-REQ", "minimum_license_type": "D"}
        )
        truck_id = truck_response.json()["id"]

        # Try to create assignment - should fail
        response = client.post(
            "/api/assignments",
            json={
                "driver_id": driver_id,
                "truck_id": truck_id,
                "assignment_date": "2025-11-10"
            }
        )
        assert response.status_code == 422
        assert "cannot operate" in response.json()["detail"]

    def test_create_assignment_driver_already_assigned(self):
        """Test creating duplicate assignment for driver on same date"""
        # Create driver
        driver_response = client.post(
            "/api/drivers",
            json={"name": "Busy Driver", "license_type": "E"}
        )
        driver_id = driver_response.json()["id"]

        # Create two trucks
        truck1_response = client.post(
            "/api/trucks",
            json={"plate": "TRUCK-1", "minimum_license_type": "A"}
        )
        truck1_id = truck1_response.json()["id"]

        truck2_response = client.post(
            "/api/trucks",
            json={"plate": "TRUCK-2", "minimum_license_type": "A"}
        )
        truck2_id = truck2_response.json()["id"]

        # Create first assignment
        client.post(
            "/api/assignments",
            json={
                "driver_id": driver_id,
                "truck_id": truck1_id,
                "assignment_date": "2025-11-15"
            }
        )

        # Try to create second assignment for same driver on same date
        response = client.post(
            "/api/assignments",
            json={
                "driver_id": driver_id,
                "truck_id": truck2_id,
                "assignment_date": "2025-11-15"
            }
        )
        assert response.status_code == 409
        assert "already assigned" in response.json()["detail"]

    def test_get_assignments_by_date(self):
        """Test filtering assignments by date"""
        # Create driver and truck
        driver_response = client.post(
            "/api/drivers",
            json={"name": "Filter Test Driver", "license_type": "C"}
        )
        driver_id = driver_response.json()["id"]

        truck_response = client.post(
            "/api/trucks",
            json={"plate": "FILTER-1", "minimum_license_type": "B"}
        )
        truck_id = truck_response.json()["id"]

        # Create assignment
        assignment_date = "2025-12-25"
        client.post(
            "/api/assignments",
            json={
                "driver_id": driver_id,
                "truck_id": truck_id,
                "assignment_date": assignment_date
            }
        )

        # Filter by date
        response = client.get(f"/api/assignments?assignment_date={assignment_date}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(a["assignment_date"] == assignment_date for a in data)
