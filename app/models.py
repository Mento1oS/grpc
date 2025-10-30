# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(200), unique=True, index=True, nullable=False)
    definition = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
