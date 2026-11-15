import json
from app.loader import Loader
from app.models import EngineMeasurement


class JSONLoader(Loader):
    def load_data(self) -> list[EngineMeasurement]:
        self.errors.clear()
        measurements = []

        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON must contain a list of measurements")

        for i, line in enumerate(data, 1):
            engine_measurement = self.parse_record(line, i)

            if engine_measurement is not None:
                measurements.append(engine_measurement)

        return measurements