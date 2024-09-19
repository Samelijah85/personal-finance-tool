import os
import secrets

from dotenv import load_dotenv

load_dotenv("app/.env")


class Settings():
    def __init__(self) -> None:
        self.MONGO_REMOTE_URI = os.getenv("MONGO_REMOTE_URI")
        self.SECRET_KEY = secrets.token_urlsafe(32)
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
