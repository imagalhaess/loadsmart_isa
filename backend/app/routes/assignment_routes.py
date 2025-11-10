"""
API routes for assignment management.
Implements RESTful endpoints following best practices.
"""
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from app.schemas.assignment_schema import (
    AssignmentCreateRequest,
    AssignmentUpdateRequest,
    AssignmentResponse
)
from app.services.assignment_service import AssignmentService
from app.models.assignment import Assignment


router = APIRouter(prefix="/assignments", tags=["assignments"])


def get_assignment_service() -> AssignmentService:
    """
    Dependency injection for AssignmentService.
    This allows easy testing and follows Dependency Inversion Principle.
    """
    from app.dependencies import get_assignment_service as get_service
    return get_service()


@router.post(
    "",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new assignment",
    description="Creates a new driver-truck assignment with validation"
)
def create_assignment(
    request: AssignmentCreateRequest,
    service: AssignmentService = Depends(get_assignment_service)
) -> AssignmentResponse:
    """
    Create a new assignment.

    Validates:
    - Driver and truck exist
    - Driver's license is compatible with truck's requirements
    - Driver is not already assigned on that date
    - Truck is not already assigned on that date

    Args:
        request: Assignment creation request data
        service: Injected assignment service

    Returns:
        AssignmentResponse: The created assignment
    """
    assignment = Assignment(
        driver_id=request.driver_id,
        truck_id=request.truck_id,
        assignment_date=request.assignment_date
    )
    created_assignment = service.create_assignment(assignment)
    return AssignmentResponse(
        id=created_assignment.id,
        driver_id=created_assignment.driver_id,
        truck_id=created_assignment.truck_id,
        assignment_date=created_assignment.assignment_date
    )


@router.get(
    "",
    response_model=List[AssignmentResponse],
    summary="Get assignments",
    description="Retrieves assignments, optionally filtered by date"
)
def get_assignments(
    assignment_date: date = Query(None, description="Filter by assignment date"),
    service: AssignmentService = Depends(get_assignment_service)
) -> List[AssignmentResponse]:
    """
    Get assignments, optionally filtered by date.

    Args:
        assignment_date: Optional date filter
        service: Injected assignment service

    Returns:
        List[AssignmentResponse]: List of assignments
    """
    if assignment_date:
        assignments = service.get_assignments_by_date(assignment_date)
    else:
        assignments = service.get_all_assignments()

    return [
        AssignmentResponse(
            id=assignment.id,
            driver_id=assignment.driver_id,
            truck_id=assignment.truck_id,
            assignment_date=assignment.assignment_date
        )
        for assignment in assignments
    ]


@router.get(
    "/{assignment_id}",
    response_model=AssignmentResponse,
    summary="Get an assignment by ID",
    description="Retrieves a specific assignment by its ID"
)
def get_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
) -> AssignmentResponse:
    """
    Get an assignment by ID.

    Args:
        assignment_id: The assignment's unique identifier
        service: Injected assignment service

    Returns:
        AssignmentResponse: The requested assignment
    """
    assignment = service.get_assignment(assignment_id)
    return AssignmentResponse(
        id=assignment.id,
        driver_id=assignment.driver_id,
        truck_id=assignment.truck_id,
        assignment_date=assignment.assignment_date
    )


@router.put(
    "/{assignment_id}",
    response_model=AssignmentResponse,
    summary="Update an assignment",
    description="Updates an existing assignment with validation"
)
def update_assignment(
    assignment_id: int,
    request: AssignmentUpdateRequest,
    service: AssignmentService = Depends(get_assignment_service)
) -> AssignmentResponse:
    """
    Update an assignment.

    Validates:
    - Assignment exists
    - Driver and truck exist
    - Driver's license is compatible with truck's requirements
    - Driver is not already assigned on that date (excluding this assignment)
    - Truck is not already assigned on that date (excluding this assignment)

    Args:
        assignment_id: The assignment's unique identifier
        request: Assignment update request data
        service: Injected assignment service

    Returns:
        AssignmentResponse: The updated assignment
    """
    assignment = Assignment(
        driver_id=request.driver_id,
        truck_id=request.truck_id,
        assignment_date=request.assignment_date
    )
    updated_assignment = service.update_assignment(assignment_id, assignment)
    return AssignmentResponse(
        id=updated_assignment.id,
        driver_id=updated_assignment.driver_id,
        truck_id=updated_assignment.truck_id,
        assignment_date=updated_assignment.assignment_date
    )


@router.delete(
    "/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an assignment",
    description="Deletes an assignment from the system"
)
def delete_assignment(
    assignment_id: int,
    service: AssignmentService = Depends(get_assignment_service)
) -> None:
    """
    Delete an assignment.

    Args:
        assignment_id: The assignment's unique identifier
        service: Injected assignment service
    """
    service.delete_assignment(assignment_id)
