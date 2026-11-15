import pytest
import pandas as pd
from app.analysis import EngineAnalyzer

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "rpm": [3500, 5000],
        "temperature": [420.5, 550.0]
    })


def test_average_rpm(sample_df):
    report = EngineAnalyzer(sample_df).generate_report()
    assert report["average_rpm"] == 4250.0


def test_min_temperature(sample_df):
    report = EngineAnalyzer(sample_df).generate_report()
    assert report["min_temperature"] == 420.5


def test_rpm_std(sample_df):
    report = EngineAnalyzer(sample_df).generate_report()
    assert report["rpm_std"] == 750.0