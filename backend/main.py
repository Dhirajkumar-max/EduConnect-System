from fastapi import FastAPI
from app.routes.school_routes import router as school_router
from app.database.connection import database

app = FastAPI()

app.include_router(school_router)

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