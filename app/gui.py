import tkinter as tk
from tkinter import filedialog

import pandas as pd
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk,
)
 
from app.json_loader import JSONLoader
from app.loader import Loader
from app.analysis import EngineAnalyzer
from app.report import export_excel
from app.plot import create_temperature_vs_rpm_figure
import csv

def run_gui():
    root = tk.Tk()
    root.title("Engineering Report Analyzer")
    root.geometry("1100x700")

    # ==============================
    # LAYOUT
    # ==============================

    sidebar = tk.Frame(root, width=270)
    sidebar.pack(side="left", fill="y", padx=15, pady=15)
    sidebar.pack_propagate(False)

    content = tk.Frame(root)
    content.pack(
        side="right",
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    # ==============================
    # APPLICATION STATE
    # ==============================

    selected_file = tk.StringVar(value="No file selected")
    status_var = tk.StringVar(value="Ready")
    report_var = tk.StringVar(value="")

    analysis_result = {}

    # ==============================
    # FUNCTIONS
    # ==============================

    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select measurement file",
            filetypes=[
                ("Data files", "*.csv *.json"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json")
            ]
        )

        if file_path:
            selected_file.set(file_path)

    def analyze_file():
        analysis_result.clear()
        report_var.set("")

        for widget in chart_area.winfo_children():
            widget.destroy()

        file_path = selected_file.get()

        if file_path == "No file selected":
            status_var.set("Please select a file first.")
            return
        
        if file_path.lower().endswith(".csv"):
            loader = Loader(file_path)
        elif file_path.lower().endswith(".json"):
            loader = JSONLoader(file_path)
        else:
            status_var.set("Unsupported file format")
            return

        try:
            measurements = loader.load_data()
        except (OSError, ValueError, csv.Error) as error:
            status_var.set(f"Error loading file: {error}")
            return
        
        if not measurements:
            status_var.set("No valid measurements to analyze")
            return

        rows = []

        for ms in measurements:
            rows.append(vars(ms))

        df = pd.DataFrame(rows)

        status_var.set(
            f"Loaded {len(measurements)} valid measurements | "
            f"Rejected {len(loader.errors)} measurements"
        )

        engine_analyzer = EngineAnalyzer(df)
        report = engine_analyzer.generate_report()

        report_var.set(
            f"Average RPM: {report['average_rpm']}\n"
            f"Minimum temperature: {report['min_temperature']} °C\n"
            f"RPM standard deviation: {report['rpm_std']}"
        )

        # Store analysis results
        analysis_result["df"] = df
        analysis_result["report"] = report
        analysis_result["errors"] = loader.errors

        # Create Matplotlib figure
        figure = create_temperature_vs_rpm_figure(df)
        analysis_result["figure"] = figure

        # Embed figure in Tkinter
        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_area
        )
        canvas.draw()

        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(
            canvas,
            chart_area,
            pack_toolbar=False
        )
        toolbar.update()

        toolbar.pack(side="bottom", fill="x")

        canvas.get_tk_widget().pack(
            side="top",
            fill="both",
            expand=True
        )

    def export_report():
        if not analysis_result:
            status_var.set("Please analyze a file first.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="engineering_report.xlsx"
        )

        if not output_path:
            return

        try:
             export_excel(analysis_result["df"], analysis_result["report"], analysis_result["errors"], output_path)
        except (OSError, ValueError) as error:
            status_var.set(f"Error exporting Excel: {error}")
            return  

        status_var.set("Excel report exported successfully.")
    def export_chart():
        if not analysis_result:
            status_var.set("Analysis results are empty")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")],
            initialfile="temperature_vs_rpm.png"
        )

        if not output_path:
            return

        figure = analysis_result["figure"]

        try:
            figure.savefig(output_path, dpi=150, bbox_inches="tight")
        except (OSError, ValueError) as error:
            status_var.set(f"Error exporting chart: {error}")
            return

        status_var.set("Chart exported successfully.")

    # ==============================
    # LEFT SIDEBAR
    # ==============================

    label = tk.Label(
        sidebar,
        text="Select measurement file",
        font=("Arial", 16),
        wraplength=240
    )
    label.pack(pady=(20, 25))

    browse_button = tk.Button(
        sidebar,
        text="Browse",
        command=select_file,
        width=18
    )
    browse_button.pack(pady=10)

    file_label = tk.Label(
        sidebar,
        textvariable=selected_file,
        wraplength=240,
        justify="center"
    )
    file_label.pack(pady=(10, 25))

    analyze_button = tk.Button(
        sidebar,
        text="Analyze",
        command=analyze_file,
        width=18
    )
    analyze_button.pack(pady=10)

    export_button = tk.Button(
        sidebar,
        text="Export Excel",
        command=export_report,
        width=18
    )
    export_button.pack(pady=10)

    chart_button = tk.Button(
        sidebar,
        text="Export Chart",
        command=export_chart,
        width=18
    )
    chart_button.pack(pady=10)

    # ==============================
    # RIGHT CONTENT
    # ==============================

    status_label = tk.Label(
        content,
        textvariable=status_var,
        anchor="w",
        justify="left"
    )
    status_label.pack(
        fill="x",
        padx=15,
        pady=(20, 15)
    )

    report_label = tk.Label(
        content,
        textvariable=report_var,
        justify="left",
        anchor="w"
    )
    report_label.pack(
        fill="x",
        padx=15,
        pady=(0, 15)
    )

    chart_area = tk.Frame(content)
    chart_area.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 10)
    )

     # Window colors
    sidebar_bg = "#26384D"
    content_bg = "#F4F6F8"

    root.configure(bg=content_bg)
    sidebar.configure(bg=sidebar_bg)
    content.configure(bg=content_bg)
    chart_area.configure(bg=content_bg)

    for widget in (label, file_label):
        widget.configure(bg=sidebar_bg, fg="white")

    for widget in (status_label, report_label):
        widget.configure(bg=content_bg, fg="#26384D", font=("Arial", 12))

    for button in (browse_button, analyze_button, export_button, chart_button):
        button.configure(font=("Arial", 12), pady=5)


    # ==============================
    # START GUI
    # ==============================


    root.mainloop()


if __name__ == "__main__":
    run_gui()
