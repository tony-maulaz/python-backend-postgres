from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_db

from crud.city import fetch_city, fetch_city_by_name

router = APIRouter()

@router.get("/{city_id}")
async def list_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await fetch_city(city_id, db)


# http://127.0.0.1:3000/api/cities/?city_name=Paris
@router.get("/")
async def get_city_by_name(
    city_name: str = Query(default=None),
    db: AsyncSession = Depends(get_db)
):
    
    return await fetch_city_by_name(db, city_name)


@router.get("/")
async def list_city(db: AsyncSession = Depends(get_db)):
    return await fetch_city_by_name(db)

