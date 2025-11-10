"""
License type enumeration and validation logic.
Implements the hierarchy of driver's license types.
"""
from enum import Enum
from typing import Set


class LicenseType(str, Enum):
    """
    Driver's license types with hierarchical levels.
    Higher license types can operate vehicles requiring lower types.
    Hierarchy: E > D > C > B > A
    """
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

    @staticmethod
    def get_license_hierarchy() -> dict[str, int]:
        """
        Returns the hierarchy level of each license type.
        Higher numbers indicate higher privilege levels.
        """
        return {
            LicenseType.A.value: 1,
            LicenseType.B.value: 2,
            LicenseType.C.value: 3,
            LicenseType.D.value: 4,
            LicenseType.E.value: 5,
        }

    def can_operate(self, required_license: "LicenseType") -> bool:
        """
        Validates if this license type can operate a vehicle requiring the specified license.

        Args:
            required_license: The minimum license type required for the vehicle

        Returns:
            bool: True if this license meets or exceeds the requirement
        """
        hierarchy = self.get_license_hierarchy()
        return hierarchy[self.value] >= hierarchy[required_license.value]

    def get_compatible_licenses(self) -> Set[str]:
        """
        Returns all license types that this license can cover.

        Returns:
            Set[str]: Set of compatible license type values
        """
        hierarchy = self.get_license_hierarchy()
        current_level = hierarchy[self.value]
        return {
            license_type
            for license_type, level in hierarchy.items()
            if level <= current_level
        }
