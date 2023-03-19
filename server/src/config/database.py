from pymongo import MongoClient
from gridfs import GridFS
from config.settings import settings
from models.user import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings


class DbSettings(BaseSettings):
    async def initialize_database(self):
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        database = client[settings.DATABASE_NAME]
        await init_beanie(database=database, document_models=[User])

    async def close_connection(self):
        self.fs.close()
        self.fs = None

    class Config:
        env_file = ".env"

class GridFSSettings():
    mongo_client = MongoClient(settings.DATABASE_URL)
    db = mongo_client[settings.DATABASE_NAME]
    file = GridFS(db)
