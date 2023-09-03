import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    def __init__(self, *args, **kwargs):
        self.DATABASE: str = os.getenv("DATABASE")
        self.AUTOFLUSH: bool = os.getenv("AUTOFLUSH")
        self.DEBUG: bool = os.getenv("DEBUG")
        self.TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL")
        self.ADMIN: str = os.getenv("ADMIN")
        self.SECRET_KEY: str = os.getenv("SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
