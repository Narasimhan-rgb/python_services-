from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health_routes import router as health_router
from app.api.profiling_routes import router as profiling_router
from app.api.detection_routes import router as detection_router
from app.api.quantum_routes import router as quantum_router


app = FastAPI(
    title="AAQ Python Profiling Service",
    description="Python FastAPI service for Polars dataset profiling and quantum-inspired support.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    health_router
)

app.include_router(
    profiling_router
)

app.include_router(
    detection_router
)

app.include_router(
    quantum_router
)


@app.get("/")
def root():
    return {
        "success": True,
        "service": "AAQ Python Profiling Service",
        "message": "Python service is running",
        "docs": "/docs"
    }