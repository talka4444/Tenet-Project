from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)

    suite_id = Column(Integer, ForeignKey("suites.id"))
    suite = relationship("Suite", back_populates="prompts")
