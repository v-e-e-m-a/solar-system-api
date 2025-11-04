from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from app.models.moon import Moon
from .route_utilities import validate_model, create_model
from ..db import db

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()

    new_planet = Planet.from_dict(request_body)
    db.session.add(new_planet)
    db.session.commit()

    response = new_planet.to_dict()

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
    planet = validate_model(Planet, id)
    
    return planet.to_dict()

# 2. ... with valid planet data to update one existing `planet` and get a success response, so that I know the API updated the `planet` data.
@planets_bp.put("/<id>")
def update_planet(id):
    planet = validate_model(Planet, id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.radius = request_body["radius"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") 

# 3. ... to delete one existing `planet` and get a success response, so that I know the API deleted the `planet` data..
@planets_bp.delete("/<id>")
def delete_planet(id):
    planet = validate_model(Planet, id)
    db.session.delete(planet)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@planets_bp.post("/<id>/moons")
def add_moon_to_existing_planet(id):
    planet = validate_model(Planet, id)
    
    request_body = request.get_json()
    print("!!!!!!!!!!!!")
    request_body["planet_id"] = planet.id
    print(request_body)
    # request_body["planet"] = planet.name

    return create_model(Moon, request_body)

@planets_bp.get("/<id>/moons")
def get_all_moons_for_one_planet(id):
    planet = validate_model(Planet, id)
    
    moons = [moon.to_dict() for moon in planet.moons]

    return moons