from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from pydantic import BaseModel
from .base import Base

class CitySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relation avec Person (One-to-Many)
    persons: Mapped[list["Person"]] = relationship("Person", back_populates="city")
