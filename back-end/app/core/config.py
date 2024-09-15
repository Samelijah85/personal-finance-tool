import os

from dotenv import load_dotenv

load_dotenv("app/.env")


class Settings():
    def __init__(self) -> None:
        self.MONGO_REMOTE_URI = os.getenv("MONGO_REMOTE_URI")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


settings = Settings()
