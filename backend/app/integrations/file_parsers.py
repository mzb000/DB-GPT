import os
import pandas as pd


def parse_file(file_path: str, original_filename: str) -> tuple[pd.DataFrame, str]:
    ext = os.path.splitext(original_filename)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(file_path, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str)

    table_name = os.path.splitext(original_filename)[0].replace(" ", "_").replace("-", "_")
    table_name = "".join(c if c.isalnum() or c == "_" else "_" for c in table_name)
    if not table_name or table_name[0].isdigit():
        table_name = "t_" + table_name

    return df, table_name
