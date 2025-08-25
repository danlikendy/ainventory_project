from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging

from .routers import data, forecasts, inventory, analytics
from ..database.init_db import init_db
from ..config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AInventory API...")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    logger.info("Shutting down AInventory API...")

app = FastAPI(
    title="AInventory API",
    description="Demand & Inventory Intelligence API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api/v1", tags=["data"])
app.include_router(forecasts.router, prefix="/api/v1", tags=["forecasts"])
app.include_router(inventory.router, prefix="/api/v1", tags=["inventory"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])

@app.get("/")
async def root():
    return {"message": "AInventory API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ainventory-api"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
