from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = f"sqlite:///./database/{settings.DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=bool(settings.AUTOFLUSH), bind=engine)
