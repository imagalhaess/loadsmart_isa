"""
Driver domain model.
Represents a driver entity with their license information.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from .license_type import LicenseType


class Driver(BaseModel):
    """
    Driver entity representing a person who can operate trucks.

    Attributes:
        id: Unique identifier for the driver
        name: Full name of the driver
        license_type: Type of driver's license held
    """
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100, description="Driver's full name")
    license_type: LicenseType = Field(..., description="Type of driver's license")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validates and normalizes the driver's name.

        Args:
            v: The name to validate

        Returns:
            str: Normalized name (stripped of extra whitespace)

        Raises:
            ValueError: If name is empty after stripping
        """
        normalized = v.strip()
        if not normalized:
            raise ValueError("Driver name cannot be empty or only whitespace")
        return normalized

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "license_type": "D"
            }
        }
