from flask import Blueprint, abort, make_response
from app.models.planet import planets

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.get("")
def get_all_planet():
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