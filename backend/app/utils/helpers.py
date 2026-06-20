import json
from datetime import datetime


def format_datetime(dt) -> str:
    if isinstance(dt, datetime):
        return dt.isoformat()
    return str(dt)


def truncate_text(text: str, max_len: int = 200) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def pretty_json(data) -> str:
    return json.dumps(data, indent=2, default=str)
