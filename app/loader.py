import csv
from app.models import EngineMeasurement

class Loader:
    def __init__(self, path):
        self.path = path

    def load_data(self) -> list[EngineMeasurement]:
        with open(self.path, "r", encoding="UTF-8", newline="") as file:
            data = csv.DictReader(file)
            measurements =[]
            for i,line in enumerate(data,1):
                try:
                    rpm = int(line["rpm"])
                    temp = float(line["temperature"])
                except ValueError:
                    print(f"Line {i}: Wrong Value")
                    continue
                measurements.append(EngineMeasurement(line["engine_id"],rpm, temp))
            return measurements

