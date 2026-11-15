from app.loader import Loader
from app.json_loader import JSONLoader

def test_load_csv():
    loader = Loader("data/measurements.csv")
    measurements = loader.load_data()

    assert len(measurements) == 2
    assert len(loader.errors) == 2

def test_load_json():
    loader = JSONLoader("data/measurements.json")
    measurements = loader.load_data()

    assert len(measurements) == 2
    assert len(loader.errors) == 0

def test_invalid_csv_row(tmp_path):
    file_path = tmp_path / "test.csv"

    data = """engine_id,rpm,temperature,measurement_id,thrust_n,measured_at
ENG-01,4000,420.5,M-001,5000,2026-11-15
ENG-02,wrong,450.0,M-002,6000,2026-11-15
"""

    file_path.write_text(data, encoding="utf-8")

    loader = Loader(file_path)
    measurements = loader.load_data()

    assert len(measurements) == 1
    assert len(loader.errors) == 1