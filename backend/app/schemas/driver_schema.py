"""
API schemas for driver-related requests and responses.
"""
from pydantic import BaseModel, Field
from app.models.license_type import LicenseType


class DriverCreateRequest(BaseModel):
    """Schema for creating a new driver"""
    name: str = Field(..., min_length=1, max_length=100, description="Driver's full name")
    license_type: LicenseType = Field(..., description="Type of driver's license")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "license_type": "D"
            }
        }


class DriverUpdateRequest(BaseModel):
    """Schema for updating a driver"""
    name: str = Field(..., min_length=1, max_length=100, description="Driver's full name")
    license_type: LicenseType = Field(..., description="Type of driver's license")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "license_type": "D"
            }
        }


class DriverResponse(BaseModel):
    """Schema for driver response"""
    id: int = Field(..., description="Driver's unique identifier")
    name: str = Field(..., description="Driver's full name")
    license_type: LicenseType = Field(..., description="Type of driver's license")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "license_type": "D"
            }
        }
