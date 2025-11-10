"""
Unit tests for license type functionality.
Tests the license hierarchy and validation logic.
"""
import pytest
from app.models.license_type import LicenseType


class TestLicenseType:
    """Test suite for LicenseType enum and its methods"""

    def test_license_hierarchy(self):
        """Test that license hierarchy is correctly defined"""
        hierarchy = LicenseType.get_license_hierarchy()

        assert hierarchy[LicenseType.A.value] == 1
        assert hierarchy[LicenseType.B.value] == 2
        assert hierarchy[LicenseType.C.value] == 3
        assert hierarchy[LicenseType.D.value] == 4
        assert hierarchy[LicenseType.E.value] == 5

    def test_can_operate_same_license(self):
        """Test that a license can operate vehicles requiring the same license"""
        assert LicenseType.C.can_operate(LicenseType.C)
        assert LicenseType.D.can_operate(LicenseType.D)

    def test_can_operate_lower_license(self):
        """Test that higher licenses can operate vehicles requiring lower licenses"""
        assert LicenseType.E.can_operate(LicenseType.A)
        assert LicenseType.E.can_operate(LicenseType.B)
        assert LicenseType.E.can_operate(LicenseType.C)
        assert LicenseType.E.can_operate(LicenseType.D)

        assert LicenseType.D.can_operate(LicenseType.A)
        assert LicenseType.D.can_operate(LicenseType.B)
        assert LicenseType.D.can_operate(LicenseType.C)

        assert LicenseType.C.can_operate(LicenseType.A)
        assert LicenseType.C.can_operate(LicenseType.B)

    def test_cannot_operate_higher_license(self):
        """Test that lower licenses cannot operate vehicles requiring higher licenses"""
        assert not LicenseType.A.can_operate(LicenseType.B)
        assert not LicenseType.A.can_operate(LicenseType.C)
        assert not LicenseType.A.can_operate(LicenseType.D)
        assert not LicenseType.A.can_operate(LicenseType.E)

        assert not LicenseType.B.can_operate(LicenseType.C)
        assert not LicenseType.B.can_operate(LicenseType.D)
        assert not LicenseType.B.can_operate(LicenseType.E)

        assert not LicenseType.C.can_operate(LicenseType.D)
        assert not LicenseType.C.can_operate(LicenseType.E)

    def test_get_compatible_licenses(self):
        """Test getting all compatible licenses for a given license type"""
        # License A can only operate A
        assert LicenseType.A.get_compatible_licenses() == {"A"}

        # License C can operate A, B, and C
        assert LicenseType.C.get_compatible_licenses() == {"A", "B", "C"}

        # License E can operate all licenses
        assert LicenseType.E.get_compatible_licenses() == {"A", "B", "C", "D", "E"}
