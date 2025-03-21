from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.db import get_db
from models.city import City

async def fetch_city(city_id: int, db: AsyncSession):
    result = await db.execute(select(City).filter(City.id == city_id))
    city = result.scalars().first()
    return city

async def fetch_city_by_name(db: AsyncSession, city_name: str=None):
    query = select(City)

    if city_name:
        query = query.filter(City.name.ilike(city_name))

    result = await db.execute(query)
    cities = result.scalars().all()
    return cities