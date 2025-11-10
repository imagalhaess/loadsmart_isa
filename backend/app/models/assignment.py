"""
Assignment domain model.
Represents the relationship between a driver and a truck for a specific date.
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field


class Assignment(BaseModel):
    """
    Assignment entity representing a driver-truck assignment for a specific date.

    Attributes:
        id: Unique identifier for the assignment
        driver_id: ID of the assigned driver
        truck_id: ID of the assigned truck
        assignment_date: Date of the assignment
    """
    id: Optional[int] = None
    driver_id: int = Field(..., gt=0, description="ID of the driver")
    truck_id: int = Field(..., gt=0, description="ID of the truck")
    assignment_date: date = Field(..., description="Date of the assignment")

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "driver_id": 1,
                "truck_id": 1,
                "assignment_date": "2025-11-10"
            }
        }
