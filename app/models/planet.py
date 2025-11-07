from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Planet(db.Model):
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    radius: Mapped[int]
    moons: Mapped[list["Moon"]] = relationship(back_populates="planet")

    def to_dict(self):
        model_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "radius": self.radius,
            "moons": []
        }

        # Return a list of moon names (not a generator) so the dict is JSON-serializable
        model_dict["moons"] = [moon.name for moon in self.moons] if self.moons else []

        return model_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(name = data_dict["name"],
                   description = data_dict["description"],
                   radius = data_dict["radius"]
                   # moon_id = data_dict.get("moon_id", None)
                   )
    