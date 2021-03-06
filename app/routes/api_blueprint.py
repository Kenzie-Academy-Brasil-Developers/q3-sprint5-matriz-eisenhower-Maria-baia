from flask import Blueprint
from app.routes.categories_blueprint import bp_categories
from app.routes.tasks_blueprint import bp_tasks

bp_api = Blueprint("bp_api", __name__)

bp_api.register_blueprint(bp_categories)
bp_api.register_blueprint(bp_tasks)