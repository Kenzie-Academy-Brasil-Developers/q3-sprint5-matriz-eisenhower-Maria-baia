import re
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import backref, relationship
from app.configs.database import db
from app.models.tasks_model import TasksModel
from app.models.categories_model import CategoriesModel
from dataclasses import dataclass

@dataclass
class TasksCategoriesModel(db.Model):
    id: int
    task: TasksModel
    category: CategoriesModel

    __tablename__ = "tasks_categories"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("TasksModel", backref=backref("task_category", uselist=False))

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("CategoriesModel", backref=backref("task_category", uselist=False))