from app.loader import Loader
from app.analysis import EngineAnalyzer
from app.plot import plot_temperature_vs_rpm
from app.report import export_excel
from app.gui import run_gui

import json
import pandas as pd
import sys

def run_cli():

    loader = Loader("data/measurements.csv")

    try:
        measurements = loader.load_data()
    except FileNotFoundError as error:
        print(f"File error: {error}")
        sys.exit(1)

    print(f"Valid measurements: {len(measurements)}")
    print(f"Rejected measurements: {len(loader.errors)}")

    with open("data/errors.json", "w", encoding="utf-8") as file:
        json.dump(loader.errors, file, indent=4)

    if not measurements:
        print("No valid measurements to analyze.")
        sys.exit(1)
        

    rows = []

    for measurement in measurements:
        rows.append(vars(measurement))

    df = pd.DataFrame(rows)

    analyzer = EngineAnalyzer(df)
    report = analyzer.generate_report()

    export_excel(df, report, loader.errors, "data/engineering_report.xlsx")

    plot_temperature_vs_rpm(df, "data/temperature_vs_rpm.png")

    print(report)

    with open("data/report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        run_gui()