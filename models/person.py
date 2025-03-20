from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from .base import Base
from pydantic import BaseModel
from typing import List, Optional
from .skill import SkillSchema
from .city import CitySchema


class PersonSchema(BaseModel):
    id: int
    name: str
    age: int
    skills: list[SkillSchema] = []
    city: Optional[CitySchema]
    #city: Optional[str]

    class Config:
        from_attributes = True

class PersonCreate(BaseModel):
    name: str
    age: int
    city_id: Optional[int] = None

class PersonSkillCreate(BaseModel):
    person_id: int
    skill_id: int


# Table Pivot pour la relation Many-to-Many (Person <-> Skill)
person_skills = Table(
    "person_skills",  # Nom de la table pivot
    Base.metadata,
    Column("person_id", Integer, ForeignKey("persons.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
    UniqueConstraint("person_id", "skill_id", name="uq_person_skill")
)

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    city_id = Column(Integer, ForeignKey("cities.id"))

    # Relation avec City (Many-to-One)
    city: Mapped["City"] = relationship("City", back_populates="persons")

    # Relation Many-to-Many avec Skill
    skills: Mapped[list["Skill"]] = relationship("Skill", secondary=person_skills, back_populates="persons")