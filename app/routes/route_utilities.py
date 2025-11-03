from flask import Blueprint, abort, make_response, request, Response
from app.models.planet import Planet
from ..db import db

def validate_model(cls, id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"message": f" {cls.__name__} id ({id}) is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(cls).order_by(cls.id)
    model = db.session.scalar(query)

    if not model:
        not_found = []
        abort(make_response(not_found, 404))
    
    return model