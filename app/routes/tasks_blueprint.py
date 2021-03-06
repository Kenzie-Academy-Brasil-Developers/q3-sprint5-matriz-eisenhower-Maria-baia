from flask import Blueprint
from app.controllers.tasks_controller import create_task, update_task, delete_task

bp_tasks = Blueprint("bp_tasks", __name__, url_prefix="/tasks")

bp_tasks.post("")(create_task)
bp_tasks.patch("/<int:id>")(update_task)
bp_tasks.delete("/<int:id>")(delete_task)