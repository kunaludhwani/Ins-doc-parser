"""
Sacha Advisor - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import upload, health
from app.db.database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered insurance document explainer"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    # Allow all origins for production (or specify your frontend URL)
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database


@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Sacha Advisor API",
        "version": settings.APP_VERSION,
        "status": "running"
    }
