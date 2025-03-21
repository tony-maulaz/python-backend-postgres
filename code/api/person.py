
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db

from crud.person import get_persons, get_persons_full, create_person, \
add_skill_to_person, add_skill_without_check, get_persons_by_id

from models.person import PersonSchema, PersonCreate, PersonSkillCreate

router = APIRouter()

@router.get("/")
async def list_persons(db: AsyncSession = Depends(get_db)):
    return await get_persons(db)

@router.get("/{person_id}")
async def list_person_by_id(person_id: int, db: AsyncSession = Depends(get_db)):
    return await get_persons_by_id(person_id, db)

@router.get("/full", response_model=list[PersonSchema])
async def list_persons_full(db: AsyncSession = Depends(get_db)):
    return await get_persons_full(db)


@router.post("/add")
async def add_person(person: PersonCreate, db: AsyncSession = Depends(get_db)):
    return await create_person(person, db)


@router.post("/addskill")
async def addskill_to_person(person_skill: PersonSkillCreate, db: AsyncSession = Depends(get_db)):
    return await add_skill_to_person(person_skill, db)


@router.post("/addskills-withoutcheck")
async def addskill_without_check(person_skill: PersonSkillCreate, db: AsyncSession = Depends(get_db)):
    return await add_skill_without_check(person_skill, db)