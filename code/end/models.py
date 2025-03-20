from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Table Pivot pour la relation Many-to-Many (Person <-> Skill)
person_skills = Table(
    "person_skills",  # Nom de la table pivot
    Base.metadata,
    Column("person_id", Integer, ForeignKey("persons.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True)
)

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relation avec Person (One-to-Many)
    persons = relationship("Person", back_populates="city")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relation Many-to-Many avec Person
    persons = relationship("Person", secondary=person_skills, back_populates="skills")

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    age = Column(Integer)
    city_id = Column(Integer, ForeignKey("cities.id"))

    # Relation avec City (Many-to-One)
    city = relationship("City", back_populates="persons")

    # Relation Many-to-Many avec Skill
    skills = relationship("Skill", secondary=person_skills, back_populates="persons")