"""Tests for shared healthcare data models."""

import sys
import os
import pytest
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))

from healthcare_models import (
    PatientDemographics,
    VitalSigns,
    Severity,
    Priority,
    ClinicalSpecialty,
)


class TestPatientDemographics:
    def test_age_calculated_from_birth_date(self):
        patient = PatientDemographics(
            patient_id="P001",
            name="John Doe",
            birth_date=date(1990, 1, 1),
            gender="male",
        )
        expected_age = date.today().year - 1990 - (
            (date.today().month, date.today().day) < (1, 1)
        )
        assert patient.age == expected_age

    def test_required_fields(self):
        with pytest.raises(Exception):
            PatientDemographics(
                patient_id="P001",
                name="John Doe",
                # missing birth_date and gender
            )


class TestVitalSigns:
    def test_valid_vital_signs(self):
        vs = VitalSigns(
            systolic_bp=120,
            diastolic_bp=80,
            heart_rate=72,
        )
        assert vs.systolic_bp == 120
        assert vs.diastolic_bp == 80
        assert vs.heart_rate == 72

    def test_systolic_bp_too_high(self):
        with pytest.raises(ValueError, match="Systolic BP"):
            VitalSigns(systolic_bp=300)

    def test_systolic_bp_too_low(self):
        with pytest.raises(ValueError, match="Systolic BP"):
            VitalSigns(systolic_bp=50)

    def test_diastolic_bp_out_of_range(self):
        with pytest.raises(ValueError, match="Diastolic BP"):
            VitalSigns(diastolic_bp=200)

    def test_heart_rate_out_of_range(self):
        with pytest.raises(ValueError, match="Heart rate"):
            VitalSigns(heart_rate=250)

    def test_none_values_are_valid(self):
        vs = VitalSigns()
        assert vs.systolic_bp is None
        assert vs.diastolic_bp is None
        assert vs.heart_rate is None


class TestEnums:
    def test_severity_values(self):
        assert Severity.LOW == "low"
        assert Severity.CRITICAL == "critical"

    def test_priority_values(self):
        assert Priority.STAT == "stat"
        assert Priority.ROUTINE == "routine"

    def test_specialty_values(self):
        assert ClinicalSpecialty.CARDIOLOGY == "cardiology"
        assert ClinicalSpecialty.EMERGENCY == "emergency"
