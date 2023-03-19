from pydantic import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    JWT_PUBLIC_KEY: str = os.environ["JWT_PUBLIC_KEY"]
    JWT_PRIVATE_KEY: str = os.environ["JWT_PRIVATE_KEY"]
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"]

settings = Settings()
