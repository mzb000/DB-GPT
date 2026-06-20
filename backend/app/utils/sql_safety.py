import re
from typing import Optional

FORBIDDEN_PATTERNS = [
    r"\bDROP\b", r"\bDELETE\b", r"\bINSERT\b", r"\bUPDATE\b",
    r"\bALTER\b", r"\bTRUNCATE\b", r"\bCREATE\b", r"\bGRANT\b",
    r"\bREVOKE\b", r"\bEXEC\b", r"\bEXECUTE\b", r"\bINTO\b",
    r"\bFILE\b", r";.*;", r"--", r"\/\*",
]


def validate_sql_readonly(sql: str) -> Optional[str]:
    sql_upper = sql.upper()
    if not re.search(r"^\s*SELECT", sql_upper):
        return "Only SELECT queries are allowed"
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, sql_upper):
            return f"Forbidden SQL keyword detected: {pattern}"
    return None


def sanitize_sql(sql: str) -> str:
    return sql.strip().rstrip(";")
