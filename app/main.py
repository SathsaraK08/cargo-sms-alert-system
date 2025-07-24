from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import uvicorn

from app.core.config import settings
from app.api.routes import auth, packages, admin, reports
from app.core.database import engine
from app.models import Base

app = FastAPI(
    title="Cargo SMS Alert System",
    description="Production-ready web application for automated multilingual SMS alerts at every package tracking stage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(packages.router, prefix="/packages", tags=["packages"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])


@app.get("/")
async def root():
    return {"message": "Cargo SMS Alert System v3", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
