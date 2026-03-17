from fragment_of_society.entities.entity import Entity
from fragment_of_society.components import Stats, Hitbox

class Character(Entity):
    def __init__(
            self,
            name: str,
            stats: Stats,
            hitbox: Hitbox,
            x: float = 0,
            y: float = 0
            ) -> None:

        super().__init__(x, y, stats, hitbox)
        self.name = name


    def __repr__(self) -> str:
        return f"Character({self.name}, id={self.id} hp={self.hp}/{self.stats.max_hp})"
