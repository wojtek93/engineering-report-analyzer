import math

class EngineMeasurement:
    def __init__(self, engine_id, rpm, temperature, measurement_id, thrust_n, measured_at):
        self.engine_id = engine_id
        self.rpm = rpm
        self.temperature = temperature
        self.measurement_id = measurement_id
        self.thrust_n = thrust_n
        self.measured_at = measured_at

    def is_valid(self) -> bool:
        if not isinstance(self.measurement_id, str):
            return False
        
        if not math.isfinite(self.temperature):
            return False
        
        return (
            self.rpm >= 0
            and self.temperature >= -273.15
            and self.thrust_n >= 0
            and bool(self.measurement_id.strip())
        )

    def is_overheated(self) -> bool:
        return self.temperature >= 500

    @property
    def get_engine_id(self) -> str:
        return self.engine_id 