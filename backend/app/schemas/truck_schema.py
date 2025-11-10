"""
API schemas for truck-related requests and responses.
"""
from pydantic import BaseModel, Field
from app.models.license_type import LicenseType


class TruckCreateRequest(BaseModel):
    """Schema for creating a new truck"""
    plate: str = Field(..., min_length=1, max_length=20, description="Truck's license plate")
    minimum_license_type: LicenseType = Field(..., description="Minimum license required")

    class Config:
        json_schema_extra = {
            "example": {
                "plate": "ABC-1234",
                "minimum_license_type": "C"
            }
        }


class TruckUpdateRequest(BaseModel):
    """Schema for updating a truck"""
    plate: str = Field(..., min_length=1, max_length=20, description="Truck's license plate")
    minimum_license_type: LicenseType = Field(..., description="Minimum license required")

    class Config:
        json_schema_extra = {
            "example": {
                "plate": "ABC-1234",
                "minimum_license_type": "C"
            }
        }


class TruckResponse(BaseModel):
    """Schema for truck response"""
    id: int = Field(..., description="Truck's unique identifier")
    plate: str = Field(..., description="Truck's license plate")
    minimum_license_type: LicenseType = Field(..., description="Minimum license required")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "plate": "ABC-1234",
                "minimum_license_type": "C"
            }
        }
