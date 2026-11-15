import pandas as pd

class EngineAnalyzer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def get_average_rpm(self) -> float:
        return float(self.df["rpm"].mean())
    
    def get_min_temperature(self) -> float:
        return float(self.df["temperature"].min())
    
    def get_rpm_std(self) -> float:
        rpm_std = self.df["rpm"].to_numpy()
        return float(rpm_std.std())
    
    def generate_report(self) -> dict:
        report={
            "average_rpm": self.get_average_rpm(),
            "min_temperature": self.get_min_temperature(),
            "rpm_std": self.get_rpm_std(),
            "valid_measurements": len(self.df)
        }
        return report