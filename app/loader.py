import csv
from app.models import EngineMeasurement

class Loader:
    def __init__(self, path):
        self.path = path
        self.errors = []

    def load_data(self) -> list[EngineMeasurement]:
        with open(self.path, "r", encoding="UTF-8", newline="") as file:
            data = csv.DictReader(file)
            measurements =[]
            for i,line in enumerate(data,2):
                try:
                    engine_id = line["engine_id"]
                    rpm = int(line["rpm"])
                    temp = float(line["temperature"])
                    measurement_id = line["measurement_id"]
                    thrust_n = int(line["thrust_n"])
                    measured_at = line["measured_at"]
                except ValueError as error:
                    self.errors.append(
                        {
                            "row": i,
                            "reason": str(error)
                        }
                    )
                    continue
                engine_measurement =  EngineMeasurement(engine_id,rpm, temp, measurement_id, thrust_n, measured_at)  
                if not engine_measurement.is_valid():
                     self.errors.append({
                        "row": i,
                        "reason": "Invalid measurement values"
                    })
                     continue
                measurements.append(engine_measurement)
            return measurements

