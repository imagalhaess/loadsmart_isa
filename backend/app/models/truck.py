"""
Truck domain model.
Represents a truck entity with its license requirements.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from .license_type import LicenseType
import re


class Truck(BaseModel):
    """
    Truck entity representing a vehicle that requires a driver.

    Attributes:
        id: Unique identifier for the truck
        plate: License plate number
        minimum_license_type: Minimum license type required to operate this truck
    """
    id: Optional[int] = None
    plate: str = Field(..., min_length=1, max_length=20, description="Truck's license plate")
    minimum_license_type: LicenseType = Field(..., description="Minimum license required to operate")

    @field_validator("plate")
    @classmethod
    def validate_plate(cls, v: str) -> str:
        """
        Validates and normalizes the truck's license plate.

        Args:
            v: The plate to validate

        Returns:
            str: Normalized plate (uppercase, stripped)

        Raises:
            ValueError: If plate is empty or contains only whitespace
        """
        normalized = v.strip().upper()
        if not normalized:
            raise ValueError("Truck plate cannot be empty or only whitespace")

        # Remove extra spaces and normalize format
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "plate": "ABC-1234",
                "minimum_license_type": "C"
            }
        }
