import os
import json
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.datasource import Datasource
from app.integrations.file_parsers import parse_file
from app.config import settings


async def process_upload(db: AsyncSession, user_id: str, file_path: str, filename: str) -> dict:
    df, table_name = parse_file(file_path, filename)
    db_path = os.path.join(settings.UPLOAD_DIR, f"uploaded_{uuid.uuid4().hex[:8]}.db")
    df.to_sql(table_name, f"sqlite:///{db_path}", if_exists="replace", index=False)

    config = json.dumps({"db_path": db_path, "table_name": table_name, "original_file": filename})
    ds = Datasource(
        user_id=user_id,
        name=filename,
        type="sqlite_upload",
        config=config,
        description=f"Uploaded from {filename} ({len(df)} rows, {len(df.columns)} columns)",
    )
    db.add(ds)
    await db.commit()
    await db.refresh(ds)

    return {
        "id": ds.id,
        "name": ds.name,
        "rows": len(df),
        "columns": list(df.columns),
        "description": ds.description,
    }
