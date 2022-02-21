from app.configs.database import db

from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

@dataclass
class CategoriesModel(db.Model):
    id: int
    name: str
    description: str

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)