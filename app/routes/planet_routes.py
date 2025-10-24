from flask import Blueprint, abort, make_response, request
from app.models.planet import Planet
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    radius = request_body["radius"]

    new_planet = Planet(name=name, description=description, radius=radius)
    db.session.add(new_planet)
    db.session.commit()

    response = {
        "id": new_planet.id,
        "name": new_planet.name,
        "despcription": new_planet.description,
        "radius": new_planet.radius
    }

    return response, 201


@planets_bp.get("")
def get_all_planet():
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)

    result_list = []

    for planet in planets:
        result_list.append(dict(
            id=planet.id,
            name=planet.name,
            description=planet.description, 
            radius=planet.radius
        ))
    
    return result_list

@planets_bp.get("/<id>")
def get_planet(id):
    planet = validate_planet(id)
    
    planet_dict = dict(
        id = planet.id,
        name = planet.name,
        description = planet.description,
        radius = planet.radius
    )
    
    return planet_dict

def validate_planet(id):
    query = db.select(Planet).order_by(Planet.id)
    planets = db.session.scalars(query)
    
    try:
        id = int(id)
    except ValueError:
        invalid = {"message": f" Planet id ({id}) is invalid."}
        abort(make_response(invalid, 400))

    for planet in planets:
        if planet.id == id:
            return planet

    response = {"message": f"Planet id ({id}) is not found."}
    abort(make_response(response, 404))