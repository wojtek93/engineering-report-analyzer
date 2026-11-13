from app.models import EngineMeasurement

measurement1 = EngineMeasurement("ENG-001", 3500, 420.5)
measurement2 = EngineMeasurement("ENG-002", -100, 610)
measurement3 = EngineMeasurement("ENG-003", 3500, -300)

print(f"Engine1: {measurement1.is_valid()} Overheated: {measurement1.is_overheated()}")
print(f"Engine2: {measurement2.is_valid()} Overheated: {measurement2.is_overheated()}")
print(f"Engine3: {measurement3.is_valid()}")