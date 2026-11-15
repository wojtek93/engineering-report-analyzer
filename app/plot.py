import pandas as pd
from matplotlib.figure import Figure


def create_temperature_vs_rpm_figure(df: pd.DataFrame) -> Figure:
    figure = Figure(figsize=(6.4, 4.8), dpi=100)
    ax = figure.add_subplot(111)

    ax.scatter(df["rpm"], df["temperature"])
    ax.set_xlabel("Engine speed (RPM)")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Engine Temperature vs RPM")
    ax.grid(True)

    figure.tight_layout()

    return figure


def plot_temperature_vs_rpm( df: pd.DataFrame, output_path: str ) -> None:
    figure = create_temperature_vs_rpm_figure(df)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")
