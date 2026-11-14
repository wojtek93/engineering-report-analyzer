import json

try:
    with open("data/measurements.json", "r", encoding="UTF-8") as file:
        measurements = json.load(file)
except (OSError, json.JSONDecodeError) as error:
     print(f"Error loading JSON: {error}")
else:
    print(f"Number of measurements: {len(measurements)}")
    for data in measurements:
        print(f"{data['engine_id']}")
