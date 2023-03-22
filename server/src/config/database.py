from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic import BaseSettings

from pymongo import MongoClient
from gridfs import GridFS

from models.user import User
from config.settings import settings


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
