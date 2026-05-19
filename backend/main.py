from fastapi import FastAPI
from app.database.connection import database

app = FastAPI()

@app.get("/")
async def home():
    return {
        "message": "EduConnect Backend Running",
        "database": str(database.name)
    }