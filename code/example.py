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

# Créer le modèle person

# Créer le modèle PersonCreate

# Créer le modèle CityOut

# Créer le modèle PersonOut 

# Créer le modèle PersonFullOut (+ city)




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

# Route GET personsfull : lire toutes les personnes avec leur skill


# Route POST add_person : ajouter une personne
