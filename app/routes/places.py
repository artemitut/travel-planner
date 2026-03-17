from flask import Blueprint, request, jsonify
from app import db
from app.models import Project, Place
import requests

places_bp = Blueprint('places', __name__)


# 🔹 helper: перевірка через API
def validate_place(external_id):
    url = f"https://api.artic.edu/api/v1/artworks/{external_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("data")


# 🔹 CREATE PLACE (додати в project)
@places_bp.route('/<int:project_id>', methods=['POST'])
def add_place(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found"}), 404

    data = request.get_json()
    external_id = data.get('external_id')

    if not external_id:
        return jsonify({"error": "external_id is required"}), 400

    # max 10 places
    if len(project.places) >= 10:
        return jsonify({"error": "Maximum 10 places allowed"}), 400

    # duplicate check
    existing = Place.query.filter_by(
        project_id=project_id,
        external_id=external_id
    ).first()

    if existing:
        return jsonify({"error": "Place already exists in project"}), 400

    # перевірка API
    api_place = validate_place(external_id)
    if not api_place:
        return jsonify({"error": "Place not found in external API"}), 400

    place = Place(
        project_id=project_id,
        external_id=external_id,
        title=api_place.get("title"),
        notes=data.get("notes")
    )

    db.session.add(place)
    db.session.commit()

    return jsonify(place_to_dict(place)), 201


# GET ALL PLACES FOR PROJECT
@places_bp.route('/<int:project_id>', methods=['GET'])
def get_places(project_id):
    project = Project.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found"}), 404

    return jsonify([place_to_dict(p) for p in project.places]), 200


# GET ONE PLACE
@places_bp.route('/<int:project_id>/<int:place_id>', methods=['GET'])
def get_place(project_id, place_id):
    place = Place.query.filter_by(
        project_id=project_id,
        id=place_id
    ).first()

    if not place:
        return jsonify({"error": "Place not found"}), 404

    return jsonify(place_to_dict(place)), 200


# UPDATE PLACE
@places_bp.route('/<int:project_id>/<int:place_id>', methods=['PUT'])
def update_place(project_id, place_id):
    place = Place.query.filter_by(
        project_id=project_id,
        id=place_id
    ).first()

    if not place:
        return jsonify({"error": "Place not found"}), 404

    data = request.get_json()

    if 'notes' in data:
        place.notes = data['notes']

    if 'visited' in data:
        place.visited = data['visited']

    db.session.commit()

    # check: are all visited → complete project
    update_project_completion(project_id)

    return jsonify(place_to_dict(place)), 200


# helper: project completion check
def update_project_completion(project_id):
    project = Project.query.get(project_id)

    if not project:
        return

    all_visited = all(place.visited for place in project.places)

    project.is_completed = all_visited
    db.session.commit()


def place_to_dict(place):
    return {
        "id": place.id,
        "project_id": place.project_id,
        "external_id": place.external_id,
        "title": place.title,
        "notes": place.notes,
        "visited": place.visited
    }
