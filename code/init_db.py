import asyncio
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from models import Base, City, Skill, Person

async def init_db():
    async with engine.begin() as conn:
        print("Suppression et recréation des tables...")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        print("Insertion des données...")

        # --- Insérer des villes ---
        cities = [
            City(name="Paris"),
            City(name="Lyon"),
            City(name="Marseille"),
            City(name="Toulouse"),
            City(name="Nice")
        ]
        session.add_all(cities)
        await session.flush()

        # --- Insérer des compétences ---
        skills = [
            Skill(name="Python"),
            Skill(name="SQL"),
            Skill(name="Java"),
            Skill(name="JavaScript"),
            Skill(name="Machine Learning")
        ]
        session.add_all(skills)
        await session.flush()

        # --- Insérer des personnes ---
        people = [
            Person(name="Alice", age=30, city_id=cities[0].id),
            Person(name="Bob", age=25, city_id=cities[1].id),
            Person(name="Charlie", age=35, city_id=cities[2].id),
            Person(name="David", age=40, city_id=cities[3].id),
            Person(name="Emma", age=28, city_id=cities[4].id),
            Person(name="Frank", age=22, city_id=cities[0].id),
            Person(name="Grace", age=33, city_id=cities[1].id),
            Person(name="Hannah", age=29, city_id=cities[2].id),
            Person(name="Isaac", age=31, city_id=cities[3].id),
            Person(name="Julia", age=27, city_id=cities[4].id),
        ]
        session.add_all(people)
        await session.flush()
        await session.commit()

        print("Base de données peuplée avec succès !")

async def init_skills():
    async with AsyncSession(engine) as session: # Créer une session
        async with session.begin(): # Débuter une transaction

            # Récupérer les compétences correctement avec SQLAlchemy ORM
            skills_result = await session.execute(select(Skill))
            skills = skills_result.scalars().all()

            # Récupérer les personnes avec leurs compétences (Many-to-Many)
            people_result = await session.execute(select(Person).options(selectinload(Person.skills)))
            people = people_result.scalars().all()

            # Associer des compétences aux personnes
            people[0].skills.append(skills[0])  # Alice sait Python
            people[1].skills.append(skills[1])  # Bob sait SQL
            people[2].skills.extend([skills[0], skills[4]])  # Charlie sait Python & ML
            people[3].skills.extend([skills[1], skills[3]])  # David sait SQL & JavaScript
            people[4].skills.extend([skills[0], skills[2]])  # Emma sait Python & Java

            await session.commit()

            print("Compétences associées avec succès !")

async def main():
    await init_db()
    await init_skills()

if __name__ == "__main__":
    asyncio.run(main())
