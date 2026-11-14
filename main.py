from app.loader import Loader
from app.analysis import EngineAnalyzer
import json
import pandas as pd

loader = Loader("data/measurements.csv")
measurements = loader.load_data()

print(f"Valid measurements: {len(measurements)}")
print(f"Rejected measurements: {len(loader.errors)}")

with open("data/errors.json", "w", encoding="utf-8") as file:
    json.dump(loader.errors, file, indent=4)

rows = []

for measurement in measurements:
    rows.append(vars(measurement))

df = pd.DataFrame(rows)

print(df)

analyzer = EngineAnalyzer(df)
report = analyzer.generate_report()

print(report)

with open("data/report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)