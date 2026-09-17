import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from app.routes.school_routes import router as school_router
from app.database.connection import database
from app.routes.user_routes import router as user_router

app = FastAPI()

# Set the deployed frontend origin through the hosting environment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(school_router)
app.include_router(user_router)


@app.exception_handler(ServerSelectionTimeoutError)
@app.exception_handler(ConfigurationError)
async def database_connection_error(_, __):
    """Return a meaningful response when the MongoDB URI is unavailable."""
    return JSONResponse(
        status_code=503,
        content={
            "detail": "The EduConnect database is currently unavailable. Please verify the MongoDB connection configuration."
        },
    )

@app.get("/health")
async def health():
    """Check API liveness without exposing configuration or requiring MongoDB."""
    return {"status": "ok"}


@app.get("/")
async def home():
    return {
        "message": "EduConnect Backend Running"
    }

@app.get("/test-db")
async def test_db():

    try:
        collections = await database.list_collection_names()

        return {
            "message": "Database Connected Successfully",
            "collections": collections
        }

    except Exception as e:
        return {
            "error": str(e)
        }
