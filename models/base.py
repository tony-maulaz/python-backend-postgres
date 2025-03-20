from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped
from .base import Base

Base = declarative_base()