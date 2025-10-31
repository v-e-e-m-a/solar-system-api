from flask import Blueprint, abort, make_response, request, Response
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
        "description": new_planet.description,
        "radius": new_planet.radius
    }

    return response, 201

# 1. ... to get a list of `planet`s, restricted to those with a match in the `description`, so that I can find a planet by a partial description.
# 2. 

@planets_bp.get("")
def get_all_planet():
    name_param = request.args.get("name")
    description_param = request.args.get("description")
    query = db.select(Planet)

    if name_param:
        query = query.where(Planet.name == name_param)
    
    if description_param:
        query = query.where(Planet.description.ilike(f"%{description_param}%"))

    query = query.order_by(Planet.id)

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

# Wave 04
# 1. ...to get one existing `planet`, so that I can see the `id`, `name`, `description`, and other data of the `planet`.

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

    response = []
    
    #{"message": f"Planet id ({id}) is not found."}
    abort(make_response(response, 404))

# 2. ... with valid planet data to update one existing `planet` and get a success response, so that I know the API updated the `planet` data.
@planets_bp.put("/<id>")
def update_planet(id):
    planet = validate_planet(id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius = request_body["radius"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") 

# 3. ... to delete one existing `planet` and get a success response, so that I know the API deleted the `planet` data..
@planets_bp.delete("/<id>")
def delete_planet(id):
    planet = validate_planet(id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")