import json
from typing import Any
import pandas as pd
from sqlalchemy import create_engine, text


def _get_url(ds_type: str, config: dict) -> str:
    if ds_type == "postgresql":
        return f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config.get('port', 5432)}/{config['database']}"
    elif ds_type == "mysql":
        return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config.get('port', 3306)}/{config['database']}"
    elif ds_type == "sqlite":
        return f"sqlite:///{config['db_path']}"
    elif ds_type == "sqlite_upload":
        return f"sqlite:///{config['db_path']}"
    elif ds_type == "mssql":
        return f"mssql+pymssql://{config['user']}:{config['password']}@{config['host']}:{config.get('port', 1433)}/{config['database']}"
    raise ValueError(f"Unsupported datasource type: {ds_type}")


async def test_connection(ds_type: str, config: dict) -> str:
    try:
        url = _get_url(ds_type, config)
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return "Connection successful"
    except Exception as e:
        raise ValueError(f"Connection failed: {e}")


async def get_schema_info(ds_type: str, config: dict) -> str:
    url = _get_url(ds_type, config)
    engine = create_engine(url)
    try:
        inspector = __import__("sqlalchemy", fromlist=["inspect"]).inspect(engine)
        tables = inspector.get_table_names()
        info_parts = []
        for table in tables[:20]:
            cols = inspector.get_columns(table)
            col_strs = [f"  - {c['name']} ({c['type']})" for c in cols]
            info_parts.append(f"Table: {table}\n" + "\n".join(col_strs))
        return "\n\n".join(info_parts) if info_parts else "No tables found"
    finally:
        engine.dispose()


async def execute_sql(ds_type: str, config: dict, sql: str) -> tuple[pd.DataFrame, list[str], list[list[Any]]]:
    url = _get_url(ds_type, config)
    engine = create_engine(url)
    try:
        df = pd.read_sql(text(sql), engine)
        columns = df.columns.tolist()
        rows = df.values.tolist()
        return df, columns, rows
    finally:
        engine.dispose()
