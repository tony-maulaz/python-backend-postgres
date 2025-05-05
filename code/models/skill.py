from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from .base import Base
from pydantic import BaseModel
from typing import List, Optional

class SkillSchema(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True # Convertir les attributs en dictionnaire


class Skill(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relation Many-to-Many avec Person
    persons: Mapped[list["Person"]] = relationship("Person", secondary="person_skill", back_populates="skills")

from .person import PersonSkill