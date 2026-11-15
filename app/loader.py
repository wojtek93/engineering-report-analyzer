import csv
from app.models import EngineMeasurement


class Loader:
    def __init__(self, path):
        self.path = path
        self.errors = []

    def parse_record(self, line, i) -> EngineMeasurement | None:
        try:
            engine_id = line["engine_id"]
            rpm = int(line["rpm"])
            temp = float(line["temperature"])
            measurement_id = line["measurement_id"]
            thrust_n = int(line["thrust_n"])
            measured_at = line["measured_at"]

        except (ValueError, KeyError, TypeError) as error:
            self.errors.append({"row": i, "reason": str(error)})
            return None

        engine_measurement = EngineMeasurement(engine_id, rpm, temp, measurement_id, thrust_n, measured_at)

        if not engine_measurement.is_valid():
            self.errors.append({"row": i, "reason": "Invalid measurement values"})
            return None

        return engine_measurement

    def load_data(self) -> list[EngineMeasurement]:
        self.errors.clear()
        measurements = []

        with open(self.path, "r", encoding="utf-8", newline="") as file:
            data = csv.DictReader(file)

            for i, line in enumerate(data, 2):
                engine_measurement = self.parse_record(line, i)

                if engine_measurement is not None:
                    measurements.append(engine_measurement)

        return measurements