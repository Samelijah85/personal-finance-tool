import secrets


class Settings():
    def __init__(self) -> None:
        self.SECRET_KEY = secrets.token_urlsafe(32)
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
