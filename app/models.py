class EngineMeasurement:
    def __init__(self, engine_id, rpm, temperature):
        self.engine_id = engine_id
        self.rpm = rpm
        self.temperature = temperature

    def is_valid(self) -> bool:
        return self.rpm >= 0 and self.temperature >= -273.15

    def is_overheated(self) -> bool:
        return self.temperature >= 500 