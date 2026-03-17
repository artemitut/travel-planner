from flask import Blueprint, request, jsonify
from app import db
from app.models import Place, Project
from datetime import datetime
from app.routes.places import validate_place, place_to_dict

projects_bp = Blueprint('projects', __name__)


def project_to_dict(project):
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "start_date": str(project.start_date) if project.start_date else None,
        "is_completed": project.is_completed
    }


@projects_bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400

    places_data = data.get('places', [])

    # max 10
    if len(places_data) > 10:
        return jsonify({"error": "Maximum 10 places allowed"}), 400

    # duplicate check
    external_ids = [p.get('external_id') for p in places_data]
    if len(external_ids) != len(set(external_ids)):
        return jsonify({"error": "Duplicate external_id in request"}), 400

    # project creation
    project = Project(
        name=data['name'],
        description=data.get('description')
    )

    db.session.add(project)
    db.session.flush()

    created_places = []

    for place_data in places_data:
        external_id = place_data.get('external_id')

        if not external_id:
            return jsonify({"error": "external_id is required"}), 400

        # API check
        api_place = validate_place(external_id)
        if not api_place:
            db.session.rollback()
            return jsonify({"error": f"Place {external_id} not found"}), 400

        place = Place(
            project_id=project.id,
            external_id=external_id,
            title=api_place.get("title"),
            notes=place_data.get("notes")
        )

        db.session.add(place)
        created_places.append(place)

    db.session.commit()

    return jsonify({
        "project": project_to_dict(project),
        "places": [place_to_dict(p) for p in created_places]
    }), 201


# GET ALL
@projects_bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()

    return jsonify([project_to_dict(p) for p in projects]), 200


# GET ONE
@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found"}), 404

    return jsonify(project_to_dict(project)), 200


# UPDATE
@projects_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found"}), 404

    data = request.get_json()

    if 'name' in data:
        project.name = data['name']

    if 'description' in data:
        project.description = data['description']

    if 'start_date' in data:
        try:
            project.start_date = datetime.strptime(
                data['start_date'], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

    db.session.commit()

    return jsonify(project_to_dict(project)), 200


# DELETE
@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found"}), 404

    visited_places = Place.query.filter_by(
        project_id=project_id, visited=True).first()

    if visited_places:
        return jsonify({
            "error": "Cannot delete project with visited places"
        }), 400

    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted"}), 200
