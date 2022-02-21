from flask import request, current_app, jsonify
from app.models.tasks_model import TasksModel
from app.models.eisenhowers_model import EisenhowersModel
from app.models.tasks_categories_model import TasksCategoriesModel
from app.models.categories_model import CategoriesModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

def create_task():
    try: 
        EisenhowersModel.insert_values()
        data = request.get_json()
        classification = ''
        importance = data["importance"]
        urgency = data["urgency"]
        if importance > 2 or urgency > 2 or importance == 0 or urgency == 0:
            return jsonify({
                "msg": {
                    "valid_options": {
                    "importance": [1, 2],
                    "urgency": [1, 2]
                    },
                    "recieved_options": {
                    "importance": importance,
                    "urgency": urgency
                    }
                }
                }), 400
        if importance == 1:
            if urgency == 1:
                classification = 1
            else:
                classification = 2
        else:
            if urgency == 1:
                classification = 3
            else:
                classification = 4

        new_task = (TasksModel(
            name=data["name"],
            description=data["description"],
            duration=data["duration"],
            importance=data["importance"],
            urgency=data["urgency"],
            eisenhower_id=classification,
        ))


        current_app.db.session.add(new_task)
        current_app.db.session.commit()

        for category in data["categories"]:
            if CategoriesModel.query.filter_by(name=category.lower()).first() == None:
                new_category = (CategoriesModel(
                    name = category.lower(), 
                    description = new_task.description
                ))

                current_app.db.session.add(new_category)
                current_app.db.session.commit()
            category_id = CategoriesModel.query.filter_by(name=category.lower()).first().id
            new_task_category = (TasksCategoriesModel(
                task_id=new_task.id,
                category_id=category_id
            ))

            current_app.db.session.add(new_task_category)
            current_app.db.session.commit()

        classification = EisenhowersModel.query.get(classification)
        categories = []
        for category in data["categories"]:
            categories.append(category.lower())

        new_data = {
            "id": new_task.id,
            "name": new_task.name,
            "description": new_task.description,
            "duration": new_task.duration,
            "classification": classification.type,
            "categories": categories
        }


        return jsonify(new_data), 201

    except IntegrityError:
        return jsonify({"msg": "task already exists!"}), 409

def update_task(id):
    try:
        data = request.get_json()

        task = TasksModel.query.get(id)

        for key, value in data.items():
            setattr(task, key, value)

        current_app.db.session.add(task)
        current_app.db.session.commit()

        classification = ''
        if task.importance == 1:
                if task.urgency == 1:
                    classification = 1
                else:
                    classification = 2
        else:
            if task.urgency == 1:
                classification = 3
            else:
                classification = 4

        classification = EisenhowersModel.query.get(classification)
        category_id = TasksCategoriesModel.query.filter_by(task_id=task.id).all()
        categories = []
        for value in category_id:
            categories.append(value.category.name)

        return {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "duration": task.duration,
                "classification": classification.type,
                "categories": categories
            }, 200

    except AttributeError:
        return jsonify({"msg": "task not found!"}), 404

def delete_task(id):
    try:
        query = TasksModel.query.get(id)

        current_app.db.session.delete(query)
        current_app.db.session.commit()

        return "", 204
    
    except UnmappedInstanceError:
        return jsonify({"msg": "category not found!"}), 404