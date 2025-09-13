from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    prompt = Column(String)
    response = Column(String, nullable=True)

    scan_id = Column(String, ForeignKey("scans.id"))
    scan = relationship("Scan", back_populates="tasks")
