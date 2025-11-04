from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

class Moon(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    radius: Mapped[int]
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))
    planet: Mapped[Optional["Planet"]] = relationship("Planet", back_populates="moons")

    def to_dict(self):
        model_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "radius": self.radius,
        }

        if self.planet:
            model_dict["planet"] = self.planet

        return model_dict
    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(name = data_dict["name"],
                   description = data_dict["description"],
                   radius = data_dict["radius"]
                   )