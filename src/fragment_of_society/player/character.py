from fragment_of_society.entities.entity import Entity
from fragment_of_society.components import Stats

class Character(Entity):
    def __init__(self,
                 name: str,
                 stats: Stats,
                 x: float = 0,
                 y: float = 0,
                 hitbox = None
                 ) -> None:

        super().__init__(stats, x, y, hitbox)
        self.name = name

    def __repr__(self) -> str:
        return f"Character({self.name}, id={self.id} hp={self.hp}/{self.stats.max_hp})"
