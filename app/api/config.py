from functools import lru_cache

from pydantic_settings import BaseSettings


import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_IDENTIFIER = os.getenv("API_IDENTIFIER")
ALGORITHMS = os.getenv("ALGORITHMS").split(",")

class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()