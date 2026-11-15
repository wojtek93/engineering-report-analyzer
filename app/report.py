import pandas as pd

def export_excel(df: pd.DataFrame, report: dict, errors: list, output_path: str) -> None:
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name="Measurements",index=False)
        pd.DataFrame([report]).to_excel( writer, sheet_name="Statistics", index=False )
        pd.DataFrame(errors).to_excel( writer, sheet_name="Errors", index=False)