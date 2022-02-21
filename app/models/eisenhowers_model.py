from app.configs.database import db

from sqlalchemy import Column, Integer, String
from dataclasses import dataclass

from sqlalchemy.orm import Session

from flask import current_app

@dataclass
class EisenhowersModel(db.Model):
    id: int
    type: str

    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    @classmethod
    def insert_values(cls):
        session: Session = current_app.db.session
        default_values = ["Do It First","Schedule It","Delegate It","Delete It"]
        values = EisenhowersModel.query.all()
        list_values_insert = []
        if not values:
            for value in default_values:
                value_insert = EisenhowersModel(**{"type":value})
                list_values_insert.append(value_insert)
            session.add_all(list_values_insert)
            session.commit()
