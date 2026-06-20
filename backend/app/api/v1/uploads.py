import os
import json
import uuid
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.datasource import Datasource
from app.api.deps import get_current_user
from app.core.exceptions import BadRequestError
from app.integrations.file_parsers import parse_file
from app.config import settings

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".csv", ".xlsx", ".xls"):
        raise BadRequestError("Only CSV and Excel files are supported")

    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{uuid.uuid4()}{ext}")
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        df, table_name = parse_file(file_path, file.filename)
        db_path = os.path.join(upload_dir, f"uploaded_{uuid.uuid4().hex[:8]}.db")
        df.to_sql(table_name, f"sqlite:///{db_path}", if_exists="replace", index=False)
    except Exception as e:
        os.remove(file_path)
        raise BadRequestError(f"Failed to parse file: {e}")

    config = json.dumps({"db_path": db_path, "table_name": table_name, "original_file": file.filename})
    ds = Datasource(
        user_id=current_user.id,
        name=file.filename,
        type="sqlite_upload",
        config=config,
        description=f"Uploaded from {file.filename} ({len(df)} rows, {len(df.columns)} columns)",
    )
    db.add(ds)
    await db.commit()
    await db.refresh(ds)

    return {
        "id": ds.id,
        "name": ds.name,
        "type": "sqlite_upload",
        "rows": len(df),
        "columns": list(df.columns),
        "description": ds.description,
    }
