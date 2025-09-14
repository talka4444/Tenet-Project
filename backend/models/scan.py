from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from db import Base

class ScanRequest(BaseModel):
    url: str
    suite: str

    @field_validator("url")
    def check_url_supported(cls, v):
        supported_urls: list = ['https://tryme.tendry.net/chat']
        if v not in supported_urls:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL not supported")
        return v

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, index=True)
    url = Column(String, index=True)
    
    tasks = relationship("Task", back_populates="scan")
