from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Suite(Base):
    __tablename__ = "suites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    prompts = relationship("Prompt", back_populates="suite")