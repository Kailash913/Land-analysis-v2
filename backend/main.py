"""
LRES Backend — Land Rate Evaluation System
FastAPI entry point with all routers mounted.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database.connection import init_db, close_db  # noqa: E402
from routers.evaluation import router as evaluation_router  # noqa: E402
from routers.reports import router as reports_router  # noqa: E402
from routers.admin import router as admin_router  # noqa: E402
from ml import preload_models  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown hooks."""
    # Startup
    await init_db()
    preload_models()
    print("LRES Backend ready")
    yield
    # Shutdown
    await close_db()
    print("LRES Backend shutting down")


app = FastAPI(
    title="LRES — Land Rate Evaluation System",
    version="1.0.0",
    description="AI-enabled geographic analysis engine for land valuation and agricultural recommendations.",
    lifespan=lifespan,
)

# CORS — allow frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(evaluation_router, prefix="/api", tags=["Evaluation"])
app.include_router(reports_router, prefix="/api", tags=["Reports"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "LRES Backend", "version": "1.0.0"}
