# from flask import Blueprint

# class Planet:
#     def __init__(self, id, name, description, radius):
#         self.id = id
#         self.name = name
#         self. description = description
#         self.radius = radius

# planets = [
#     Planet(1, "Earth", "Our home planet", 6371),
#     Planet(2, "Mars", "cold and rocky", 3390,),
#     Planet(3, "Jupiter", "The largest planet in our Solar System", 69911),
#     Planet(4, "Mercury", "The smallest planet in our Solar System", 2440)
# ]

from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Planet(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    radius: Mapped[int]