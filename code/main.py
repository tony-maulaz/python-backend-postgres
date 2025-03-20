from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import Person, Base, City, Skill, person_skills

app = FastAPI()

class SkillSchema(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

class CitySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

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

@app.get("/persons")
async def get_persons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Person).order_by(Person.id))
    persons = result.scalars().all()
    return persons

@app.get("/persons-full", response_model=list[PersonSchema])
async def get_persons(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Person).order_by(Person.id)
        .options(joinedload(Person.skills))
        .options(joinedload(Person.city))
    )
    persons = result.unique().scalars().all()

    # Permet de transformer les objets en dictionnaires
    # pour simplifier la sérialisation en JSON
    rep = [ 
        {
            **person.__dict__,
            "city": person.city.name if person.city else None
        }
        for person in persons
    ]
    return persons

@app.get("/city/{city_id}")
async def get_city(city_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(City).filter(City.id == city_id))
    city = result.scalars().first()
    return city

# http://127.0.0.1:3000/cities/?city_name=Paris
@app.get("/cities/")
async def get_city_by_name(city_name: str=None, db: AsyncSession = Depends(get_db)):
    query = select(City)

    if city_name:
        query = query.filter(City.name.ilike(city_name))

    result = await db.execute(query)
    cities = result.scalars().all()
    return cities


@app.post("/addperson")
async def create_person(person: PersonCreate, db: AsyncSession = Depends(get_db)):
    new_user = Person(name=person.name, age=person.age, city_id=person.city_id)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@app.post("/addpersonskill")
def add_person_skill(association: PersonSkillCreate, db: AsyncSession = Depends(get_db)):
    person = db.query(Person).filter(Person.id == association.person_id).first()
    skill = db.query(Skill).filter(Skill.id == association.skill_id).first()
    if not person or not skill:
        raise HTTPException(status_code=404, detail="Person or Skill not found")
    
    person.skills.append(skill)  # Ajout de la compétence
    db.commit()
    return {"message": "Skill added to person"}

@app.post("/addskills")
async def add_skill_to_person(person_skill: PersonSkillCreate, db: AsyncSession = Depends(get_db)):
    # Vérifier si la personne existe
    person_result = await db.execute(select(Person).filter(Person.id == person_skill.person_id))
    person = person_result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    # Vérifier si la compétence existe
    skill_result = await db.execute(select(Skill).filter(Skill.id == person_skill.skill_id))
    skill = skill_result.scalars().first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Vérifier si la personne a déjà cette compétence
    existing_result = await db.execute(
        select(person_skills)
        .where(person_skills.c.person_id == person_skill.person_id)
        .where(person_skills.c.skill_id == person_skill.skill_id)
    )
    existing_skill = existing_result.fetchone()
    
    if existing_skill:
        raise HTTPException(status_code=400, detail="Person already has this skill")

    # Ajouter la relation dans la table pivot `person_skills`
    stmt = person_skills.insert().values(person_id=person_skill.person_id, skill_id=person_skill.skill_id)
    await db.execute(stmt)
    await db.commit()

    return {"message": "Skill added to person successfully"}

@app.post("/addskills-withoutcheck")
async def add_skill_without_check(person_skill: PersonSkillCreate, db: AsyncSession = Depends(get_db)):
    try:
        stmt = person_skills.insert().values(person_id=person_skill.person_id, skill_id=person_skill.skill_id)
        await db.execute(stmt)
        await db.commit()
        return {"message": "Skill added to person successfully"}

    except IntegrityError:
        # Gestion des erreurs SQL : Clé étrangère ou contrainte UNIQUE
        await db.rollback()
        raise HTTPException(status_code=400, detail="Person not found, Skill not found, or Skill already assigned")