from flask import Blueprint

from app.controllers.categories_controller import create_categorie, update_category, delete_category, get_categories

bp_categories = Blueprint("bp_categories", __name__, url_prefix="/")

bp_categories.post("/categories")(create_categorie)
bp_categories.patch("categories/<int:id>")(update_category)
bp_categories.delete("categories/<int:id>")(delete_category)
bp_categories.get("")(get_categories)