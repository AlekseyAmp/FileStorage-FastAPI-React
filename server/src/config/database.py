from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic import BaseSettings

from models import user, file, history, statistic
from config.settings import settings


class DbSettings(BaseSettings):
    async def initialize_database(self):
        client = AsyncIOMotorClient(settings.DATABASE_URL)
        database = client[settings.DATABASE_NAME]
        await init_beanie(database=database,
                          document_models=[user.User,
                                           file.File,
                                           history.FileHistory,
                                           history.UserHistory,
                                           statistic.TodayStatistic])

    class Config:
        env_file = ".env"
