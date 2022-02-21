from unicodedata import category
from flask import request, current_app, jsonify
from app.models.categories_model import CategoriesModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from app.models.tasks_categories_model import TasksCategoriesModel
from app.models.tasks_model import TasksModel

def create_categorie():
    try:
        data = request.get_json()

        new_categorie = (CategoriesModel(
            name = data["name"].lower(), 
            description = data["description"]
        ))

        current_app.db.session.add(new_categorie)
        current_app.db.session.commit()

        return jsonify(new_categorie), 201
    except IntegrityError:
        return jsonify({"msg": "category already exists!"}), 409

def update_category(id):
    try:
        data = request.get_json()

        category = CategoriesModel.query.get(id)

        for key, value in data.items():
            setattr(category, key, value)

        current_app.db.session.add(category)
        current_app.db.session.commit()

        return {
            "id": category.id,
            "name": category.name,
            "description": category.description
        }, 200
    except AttributeError:
        return jsonify({"msg": "category not found!"}), 404

def delete_category(id):
    try:
        query = CategoriesModel.query.get(id)

        current_app.db.session.delete(query)
        current_app.db.session.commit()

        return "", 204
    except UnmappedInstanceError:
        return jsonify({"msg": "category not found!"}), 404

def get_categories():
    categories = CategoriesModel.query.all()
    result = []
    for  category in categories:
        cat = current_app.db.session.query(TasksModel, CategoriesModel).select_from(TasksModel).join(TasksCategoriesModel).join(CategoriesModel).filter_by(id = category.id).all()
        tasks = []
        for c in cat:
            print("C ", c)
            tasks.append({
                "id": c[0].id,
                "name": c[0].name,
                "description": c[0].description,
                "duration": c[0].duration,
                "classification": c[0].eisenhower.type
            })
        result.append({
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "tasks": tasks
        })
    return jsonify(result), 200