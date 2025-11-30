"""
Sacha Advisor - FastAPI Backend
Main application entry point
"""
from app.routers import acknowledge
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import upload, health, translate
from app.db.database import init_db
from app.db.supabase import init_db as init_supabase_db, close_pool

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered insurance document explainer with multilingual support"
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

# Initialize databases


@app.on_event("startup")
async def startup_event():
    """Initialize SQLite (legacy) and Supabase (production) databases"""
    init_db()  # Legacy SQLite for backward compatibility

    # Try to initialize Supabase, but don't crash if it fails
    try:
        await init_supabase_db()  # Production Supabase PostgreSQL
    except Exception as e:
        print(f"⚠️  Supabase connection unavailable: {str(e)}")
        print("   Continuing with SQLite only. Analytics will not be logged to Supabase.")


@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully close Supabase connection pool"""
    await close_pool()

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(translate.router, prefix="/api", tags=["Translation"])

# Import and include acknowledge router
app.include_router(acknowledge.router, prefix="/api", tags=["Acknowledgment"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Sacha Advisor API",
        "version": settings.APP_VERSION,
        "status": "running"
    }
