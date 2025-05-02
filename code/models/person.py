from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from .base import Base
from pydantic import BaseModel
from typing import Optional


class PersonSchema(BaseModel):
    id: int
    name: str
    age: int
    skills: list["SkillSchema"] = []
    city: Optional["CitySchema"]
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


class PersonSkill(Base):
    __tablename__ = "person_skills"

    person_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)

    # Contraintes d'unicité (équivalent à UniqueConstraint)
    __table_args__ = (
        UniqueConstraint("person_id", "skill_id", name="uq_person_skill"),
    )

    # Optionnel : relations vers les modèles Person et Skill
    person = relationship("Person", back_populates="person_skills")
    skill = relationship("Skill", back_populates="skill_persons")

    skill_persons = relationship("PersonSkill", back_populates="skill")


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


# Importer les classes SkillSchema et CitySchema en lazy loading
# Pour éviter cet import, il faut faire un dossier schemas et mettre les fichiers dedans
from .skill import SkillSchema
from .city import CitySchema    