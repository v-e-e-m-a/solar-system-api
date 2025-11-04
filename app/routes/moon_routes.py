from flask import Blueprint, abort, make_response, request, Response
from app.models.moon import Moon
from .route_utilities import validate_model
from ..db import db

moons_bp = Blueprint("moons_bp", __name__, url_prefix="/moons")