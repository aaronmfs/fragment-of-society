from fragment_of_society.entities.entity import Entity
from fragment_of_society.components.stats import Stats

class Character(Entity):
    def __init__(self,
                 name: str,
                 stats: Stats,
                 speed: float = 650,
                 x: float = 0,
                 y: float = 0
                 ) -> None:

        super().__init__(stats, x, y)
        self.name = name
        self.speed = speed

    def __repr__(self) -> str:
        return f"Character({self.name}, hp={self.hp}/{self.stats.max_hp})"
