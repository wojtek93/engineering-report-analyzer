import pytest
from app.models import EngineMeasurement

@pytest.mark.parametrize("measurement_id", [None, 123, "", "   "])
def test_invalid_measurement_id(measurement_id):
    measurement = EngineMeasurement("ENG-01", 4000, 420.5, measurement_id, 5000, "2026-11-15")
    assert measurement.is_valid() is False

def test_valid_measurement():
    measurement = EngineMeasurement("ENG-01", 4000, 420.5, "M-001", 5000, "2026-11-15")
    assert measurement.is_valid() is True

@pytest.mark.parametrize("temperature", [float("nan"), float("inf"), float("-inf")])
def test_invalid_temperature(temperature):
    measurement = EngineMeasurement("ENG-01", 4000, temperature, "M-001", 5000, "2026-11-15")
    assert measurement.is_valid() is False

@pytest.mark.parametrize("engine_id, measured_at", [("", "2026-11-15"), (None, "2026-11-15"), ("ENG-01", ""), ("ENG-01", None)])
def test_invalid_required_fields(engine_id, measured_at):
    measurement = EngineMeasurement(engine_id, 4000, 420.5, "M-001", 5000, measured_at)
    assert measurement.is_valid() is False