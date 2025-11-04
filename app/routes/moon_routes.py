from flask import Blueprint, abort, make_response, request, Response
from app.models.moon import Moon
from .route_utilities import validate_model, create_model
from ..db import db

moons_bp = Blueprint("moons_bp", __name__, url_prefix="/moons")

@moons_bp.post("")
def create_moon():
    request_body = request.get_json()

    return create_model(Moon, request_body)


