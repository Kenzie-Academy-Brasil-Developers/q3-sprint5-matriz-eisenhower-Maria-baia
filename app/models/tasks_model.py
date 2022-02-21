from time import clock_settime
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from app.models.eisenhowers_model import EisenhowersModel
from dataclasses import dataclass

@dataclass
class TasksModel(db.Model):
    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhower: EisenhowersModel

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)

    eisenhower = relationship("EisenhowersModel", backref=backref("task", uselist=False))