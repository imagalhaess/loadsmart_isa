"""
API schemas for assignment-related requests and responses.
"""
from datetime import date
from pydantic import BaseModel, Field


class AssignmentCreateRequest(BaseModel):
    """Schema for creating a new assignment"""
    driver_id: int = Field(..., gt=0, description="ID of the driver")
    truck_id: int = Field(..., gt=0, description="ID of the truck")
    assignment_date: date = Field(..., description="Date of the assignment")

    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "truck_id": 1,
                "assignment_date": "2025-11-10"
            }
        }


class AssignmentUpdateRequest(BaseModel):
    """Schema for updating an assignment"""
    driver_id: int = Field(..., gt=0, description="ID of the driver")
    truck_id: int = Field(..., gt=0, description="ID of the truck")
    assignment_date: date = Field(..., description="Date of the assignment")

    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "truck_id": 1,
                "assignment_date": "2025-11-10"
            }
        }


class AssignmentResponse(BaseModel):
    """Schema for assignment response"""
    id: int = Field(..., description="Assignment's unique identifier")
    driver_id: int = Field(..., description="ID of the driver")
    truck_id: int = Field(..., description="ID of the truck")
    assignment_date: date = Field(..., description="Date of the assignment")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "driver_id": 1,
                "truck_id": 1,
                "assignment_date": "2025-11-10"
            }
        }
