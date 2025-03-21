from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from sqlalchemy.orm import joinedload
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from models.person import Person, PersonSkillCreate, PersonCreate, person_skills
from models.skill import Skill

async def get_persons(db: AsyncSession):
    result = await db.execute(select(Person).order_by(Person.id))
    persons = result.scalars().all()
    return persons

async def get_persons_by_id(person_id: int, db: AsyncSession):
    result = await db.execute(select(Person).filter(Person.id == person_id))
    person = result.scalars().first()
    return person

async def get_persons_full(db: AsyncSession):
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

async def create_person(person: PersonCreate, db: AsyncSession):
    new_user = Person(name=person.name, age=person.age, city_id=person.city_id)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def add_skill_to_person(person_skill: PersonSkillCreate, db: AsyncSession):
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


async def add_skill_without_check(person_skill: PersonSkillCreate, db: AsyncSession):
    try:
        stmt = person_skills.insert().values(person_id=person_skill.person_id, skill_id=person_skill.skill_id)
        await db.execute(stmt)
        await db.commit()
        return {"message": "Skill added to person successfully"}

    except IntegrityError:
        # Gestion des erreurs SQL : Clé étrangère ou contrainte UNIQUE
        await db.rollback()
        raise HTTPException(status_code=400, detail="Person not found, Skill not found, or Skill already assigned")