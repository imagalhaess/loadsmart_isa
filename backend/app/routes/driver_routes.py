"""
API routes for driver management.
Implements RESTful endpoints following best practices.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.driver_schema import DriverCreateRequest, DriverUpdateRequest, DriverResponse
from app.services.driver_service import DriverService
from app.models.driver import Driver


router = APIRouter(prefix="/drivers", tags=["drivers"])


def get_driver_service() -> DriverService:
    """
    Dependency injection for DriverService.
    This allows easy testing and follows Dependency Inversion Principle.
    """
    from app.dependencies import get_driver_service as get_service
    return get_service()


@router.post(
    "",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new driver",
    description="Creates a new driver with the provided name and license type"
)
def create_driver(
    request: DriverCreateRequest,
    service: DriverService = Depends(get_driver_service)
) -> DriverResponse:
    """
    Create a new driver.

    Args:
        request: Driver creation request data
        service: Injected driver service

    Returns:
        DriverResponse: The created driver
    """
    driver = Driver(name=request.name, license_type=request.license_type)
    created_driver = service.create_driver(driver)
    return DriverResponse(
        id=created_driver.id,
        name=created_driver.name,
        license_type=created_driver.license_type
    )


@router.get(
    "",
    response_model=List[DriverResponse],
    summary="Get all drivers",
    description="Retrieves a list of all drivers"
)
def get_all_drivers(
    service: DriverService = Depends(get_driver_service)
) -> List[DriverResponse]:
    """
    Get all drivers.

    Args:
        service: Injected driver service

    Returns:
        List[DriverResponse]: List of all drivers
    """
    drivers = service.get_all_drivers()
    return [
        DriverResponse(id=driver.id, name=driver.name, license_type=driver.license_type)
        for driver in drivers
    ]


@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
    summary="Get a driver by ID",
    description="Retrieves a specific driver by their ID"
)
def get_driver(
    driver_id: int,
    service: DriverService = Depends(get_driver_service)
) -> DriverResponse:
    """
    Get a driver by ID.

    Args:
        driver_id: The driver's unique identifier
        service: Injected driver service

    Returns:
        DriverResponse: The requested driver
    """
    driver = service.get_driver(driver_id)
    return DriverResponse(
        id=driver.id,
        name=driver.name,
        license_type=driver.license_type
    )


@router.put(
    "/{driver_id}",
    response_model=DriverResponse,
    summary="Update a driver",
    description="Updates an existing driver's information"
)
def update_driver(
    driver_id: int,
    request: DriverUpdateRequest,
    service: DriverService = Depends(get_driver_service)
) -> DriverResponse:
    """
    Update a driver.

    Args:
        driver_id: The driver's unique identifier
        request: Driver update request data
        service: Injected driver service

    Returns:
        DriverResponse: The updated driver
    """
    driver = Driver(name=request.name, license_type=request.license_type)
    updated_driver = service.update_driver(driver_id, driver)
    return DriverResponse(
        id=updated_driver.id,
        name=updated_driver.name,
        license_type=updated_driver.license_type
    )


@router.delete(
    "/{driver_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a driver",
    description="Deletes a driver from the system"
)
def delete_driver(
    driver_id: int,
    service: DriverService = Depends(get_driver_service)
) -> None:
    """
    Delete a driver.

    Args:
        driver_id: The driver's unique identifier
        service: Injected driver service
    """
    service.delete_driver(driver_id)
