from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Person, City, Skill
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio

app = FastAPI()

# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
# asyncio.run(init_db())     

# Base.metadata.create_all(bind=engine)


# Définition du schéma de données pour les requêtes
class PersonCreate(BaseModel):
    nom: str
    prenom: str
    age: int
    city_id: int 

# Fonction pour récupérer une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async
# async def get_db():
#     async with SessionLocal() as session:
#         yield session

# Route GET - Liste des personnes
@app.get("/getpersons")
def get_persons(db: Session = Depends(get_db)):
    return db.query(Person).all()

# async def get_persons(db: AsyncSession = Depends(get_db)):
#     async with db.begin():
#         result = await db.execute(select(Person))
#         persons = result.scalars().all()
#     return persons


# Route POST - Ajouter une personne
@app.post("/addperson")
def add_person(person: PersonCreate, db: Session = Depends(get_db)):
    new_person = Person(nom=person.nom, prenom=person.prenom, age=person.age, city_id=person.city_id)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


class CityCreate(BaseModel):
    name: str

@app.post("/addcity")
def add_city(city: CityCreate, db: Session = Depends(get_db)):
    new_city = City(name=city.name)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city

@app.get("/getcities")
def get_cities(db: Session = Depends(get_db)):
    return db.query(City).all()


class SkillCreate(BaseModel):
    name: str

@app.post("/addskill")
def add_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    new_skill = Skill(name=skill.name)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

@app.get("/getskills")
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()


class PersonSkillAssociation(BaseModel):
    person_id: int
    skill_id: int

@app.post("/addpersonskill")
def add_person_skill(association: PersonSkillAssociation, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == association.person_id).first()
    skill = db.query(Skill).filter(Skill.id == association.skill_id).first()
    if not person or not skill:
        raise HTTPException(status_code=404, detail="Person or Skill not found")
    
    person.skills.append(skill)  # Ajout de la compétence
    db.commit()
    return {"message": "Skill added to person"}