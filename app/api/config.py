from pydantic_settings import BaseSettings


import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    WEBHOOK_SECRET: str
    ENV: str

    class Config:
        env_file = ".env"

if os.path.exists(".env.local"):
    load_dotenv(".env.local")

settings = Settings()
