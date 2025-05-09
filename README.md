# Théorie sur SQL Alchemy
## Introduction
SQLAlchemy est une bibliothèque Python qui fournit des outils pour travailler avec des bases de données relationnelles. SQLAlchemy est un ORM (Object Relational Mapper) qui permet de manipuler des bases de données relationnelles en utilisant des objets Python.

## Définitions
### Une transaction
C'est un ensemble d’opérations SQL exécutées comme un bloc unique.
- Regroupe plusieurs INSERT, UPDATE, DELETE dans un seul bloc.
- Assure que les modifications sont enregistrées uniquement si tout est OK.
- Permet d'annuler les changements si une erreur survient (ROLLBACK).
- Doit être validée avec commit() pour que les modifications soient sauvegardées.

### Une session
Représente une connexion active entre ton application et la base de données.
- Gère les interactions avec la base (requêtes SELECT, INSERT, UPDATE, DELETE).
- Maintient un cache temporaire des objets récupérés/modifiés.
- Assure que les connexions sont bien fermées après usage.
- Ne valide pas les changements immédiatement en base (utilisation de commit() nécessaire).

### Commit
Valide les changements effectués dans la base de données.

### Flush
Synchronise les objets en mémoire avec la base de données.
Un flush ne valide pas les changements en base, il les prépare pour un commit ultérieur.

# Docker
```bash
docker-compose up -d
docker exec -it backend-python bash
```

Pour afficher les logs des containers :
```bash
docker-compose logs -f -n10
```

# Base de données (en mode cli)
## Création de la base de données
Pour se connecteur en CLI : 
```bash
docker exec -it db_python psql -U postgres -d mydb
```

Commandes de base pour postgres cli :
- `\l` : lister les bases de données
- `\dt` : lister les tables
- `\d table_name` : afficher les colonnes d'une table
- `\q` : quitter
- `select * from table_name;` : afficher le contenu d'une table

# Python
## Installation des dépendances
```bash
poetry install --no-root
```

## Création de la base de données (tables)
```bash
poetry run python init_db.py
```

## Lancement du serveur
### Programme example
```bash
poetry run uvicorn example:app --host 0.0.0.0 --port 3000 --reload
```

### Programme full
```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

### Swagger et documentation
```bash
http://127.0.0.1:3000/docs
http://127.0.0.1:3000/redoc
```


## Test des routes
```bash
http://127.0.0.1:3000/api/persons/full

http://127.0.0.1:3000/api/persons

http://127.0.0.1:3000/api/persons/1

curl -X POST http://127.0.0.1:3000/api/persons/add -H "Content-Type: application/json" -d '{"name": "Doe", "age": 30, "city_id": 1}'

curl -X POST http://127.0.0.1:3000/api/persons/addskill -H "Content-Type: application/json" -d '{"person_id": 1, "skill_id": 2}'


http://127.0.0.1:3000/api/cities/
http://127.0.0.1:3000/api/cities/1
http://127.0.0.1:3000/api/cities/?city_name=Paris
```

