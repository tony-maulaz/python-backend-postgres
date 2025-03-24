from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, Mapped
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, joinedload

# 🔌 Configuration de la base PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:password@db:5432/mydb"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Modèles ORM
class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    # Relation avec Person (One-to-Many)
    persons: Mapped[list["Person"]] = relationship("Person", back_populates="city")

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    city_id = Column(Integer, ForeignKey("cities.id"))

    city: Mapped["City"] = relationship("City", back_populates="persons")

# Schémas Pydantic
class PersonCreate(BaseModel):
    name: str
    age: int
    city_id: Optional[int] = None

class CityOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class PersonOut(BaseModel):
    id: int
    name: str
    age: int
    class Config:
        from_attributes = True

class PersonFullOut(BaseModel):
    id: int
    name: str
    age: int
    city: CityOut
    class Config:
        from_attributes = True

# Dépendance pour la DB
async def get_db():
    async with SessionLocal() as session:
        yield session

# App FastAPI
app = FastAPI()

# Route GET : lire toutes les personnes
@app.get("/persons", response_model=list[PersonOut])
async def list_persons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Person).order_by(Person.id))
    persons = result.scalars().all()
    return persons

# Route GET : lire toutes les personnes avec leur skill
@app.get("/personsfull", response_model=list[PersonFullOut])
async def list_persons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Person).
        options(joinedload(Person.city)).
        order_by(Person.id))
    persons = result.scalars().all()
    return persons

# Route POST : ajouter une personne
@app.post("/add_person", response_model=PersonOut)
async def add_person(person: PersonCreate, db: AsyncSession = Depends(get_db)):
    db_person = Person(name=person.name, age=person.age, city_id=person.city_id)
    db.add(db_person)
    await db.commit()
    await db.refresh(db_person)
    return db_person