from fragment_of_society.entities.entity import Entity

class Character(Entity):
    def __init__(self, name:str, stats, speed: float = 650, x: float = 0, y: float = 0) -> None:
        super().__init__(stats, x, y)
        self.name = name
        self.speed = speed
