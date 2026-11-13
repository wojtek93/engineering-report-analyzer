from app.models import EngineMeasurement
from app.loader import Loader

loadData = Loader("data/measurements.csv")
measurements = loadData.load_data()

for measurement in measurements:
    name = measurement.engine_id
    print(f"{name}: {measurement.is_valid()}")