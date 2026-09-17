import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "educonnect")

if not MONGO_URL:
    raise RuntimeError("Set MONGO_URL to your MongoDB connection URI.")

client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000)

database = client[DATABASE_NAME]