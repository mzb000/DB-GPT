from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.core.events import seed_default_user
from app.api.v1 import auth, datasources, queries, chat, skills, reports, dashboards, uploads, settings as settings_router, search, favorites, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_default_user()
    yield


app = FastAPI(title="DB-GPT API", version="1.0.0", lifespan=lifespan)

origins = [o.strip() for o in settings.BACKEND_CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(datasources.router, prefix="/api/v1/datasources", tags=["Datasources"])
app.include_router(queries.router, prefix="/api/v1/queries", tags=["Queries"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(skills.router, prefix="/api/v1/skills", tags=["Skills"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(dashboards.router, prefix="/api/v1/dashboards", tags=["Dashboards"])
app.include_router(uploads.router, prefix="/api/v1/uploads", tags=["Uploads"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(favorites.router, prefix="/api/v1/favorites", tags=["Favorites"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/api/health")
async def health():
    return {"status": "ok"}
