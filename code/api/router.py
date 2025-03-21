from fastapi import APIRouter
from api import person, city

router = APIRouter()

router.include_router(person.router, prefix="/persons", tags=["Persons"])
router.include_router(city.router, prefix="/cities", tags=["Cities"])
#router.include_router(skill.router, prefix="/skills", tags=["Skills"])