from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


from .Enums import StatusEnum

Base = declarative_base()


class Entity(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(50), nullable=False, index=True, default=StatusEnum.ACTIVE)
    created_at = Column(DateTime(timezone=True), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_by = Column(String(50), nullable=False, index=True)
    updated_by = Column(String(50), nullable=False, index=True)
