"""
API routes for truck management.
Implements RESTful endpoints following best practices.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.truck_schema import TruckCreateRequest, TruckUpdateRequest, TruckResponse
from app.services.truck_service import TruckService
from app.models.truck import Truck


router = APIRouter(prefix="/trucks", tags=["trucks"])


def get_truck_service() -> TruckService:
    """
    Dependency injection for TruckService.
    This allows easy testing and follows Dependency Inversion Principle.
    """
    from app.dependencies import get_truck_service as get_service
    return get_service()


@router.post(
    "",
    response_model=TruckResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new truck",
    description="Creates a new truck with the provided plate and minimum license type"
)
def create_truck(
    request: TruckCreateRequest,
    service: TruckService = Depends(get_truck_service)
) -> TruckResponse:
    """
    Create a new truck.

    Args:
        request: Truck creation request data
        service: Injected truck service

    Returns:
        TruckResponse: The created truck
    """
    truck = Truck(plate=request.plate, minimum_license_type=request.minimum_license_type)
    created_truck = service.create_truck(truck)
    return TruckResponse(
        id=created_truck.id,
        plate=created_truck.plate,
        minimum_license_type=created_truck.minimum_license_type
    )


@router.get(
    "",
    response_model=List[TruckResponse],
    summary="Get all trucks",
    description="Retrieves a list of all trucks"
)
def get_all_trucks(
    service: TruckService = Depends(get_truck_service)
) -> List[TruckResponse]:
    """
    Get all trucks.

    Args:
        service: Injected truck service

    Returns:
        List[TruckResponse]: List of all trucks
    """
    trucks = service.get_all_trucks()
    return [
        TruckResponse(
            id=truck.id,
            plate=truck.plate,
            minimum_license_type=truck.minimum_license_type
        )
        for truck in trucks
    ]


@router.get(
    "/{truck_id}",
    response_model=TruckResponse,
    summary="Get a truck by ID",
    description="Retrieves a specific truck by its ID"
)
def get_truck(
    truck_id: int,
    service: TruckService = Depends(get_truck_service)
) -> TruckResponse:
    """
    Get a truck by ID.

    Args:
        truck_id: The truck's unique identifier
        service: Injected truck service

    Returns:
        TruckResponse: The requested truck
    """
    truck = service.get_truck(truck_id)
    return TruckResponse(
        id=truck.id,
        plate=truck.plate,
        minimum_license_type=truck.minimum_license_type
    )


@router.put(
    "/{truck_id}",
    response_model=TruckResponse,
    summary="Update a truck",
    description="Updates an existing truck's information"
)
def update_truck(
    truck_id: int,
    request: TruckUpdateRequest,
    service: TruckService = Depends(get_truck_service)
) -> TruckResponse:
    """
    Update a truck.

    Args:
        truck_id: The truck's unique identifier
        request: Truck update request data
        service: Injected truck service

    Returns:
        TruckResponse: The updated truck
    """
    truck = Truck(plate=request.plate, minimum_license_type=request.minimum_license_type)
    updated_truck = service.update_truck(truck_id, truck)
    return TruckResponse(
        id=updated_truck.id,
        plate=updated_truck.plate,
        minimum_license_type=updated_truck.minimum_license_type
    )


@router.delete(
    "/{truck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a truck",
    description="Deletes a truck from the system"
)
def delete_truck(
    truck_id: int,
    service: TruckService = Depends(get_truck_service)
) -> None:
    """
    Delete a truck.

    Args:
        truck_id: The truck's unique identifier
        service: Injected truck service
    """
    service.delete_truck(truck_id)
